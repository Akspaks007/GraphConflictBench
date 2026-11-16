"""Optional Gemini REST callbacks for the official native LightRAG SDK.

Single text generateContent/embedContent calls; no tools, files, model discovery,
countTokens probes, automatic retries or project/billing modifications.
"""

import hashlib
import json
import os
import re
import uuid

from .environment import install_log_redaction, redact, redact_bytes, register_secret
from .gemini_control import GeminiControl, GeminiError
from .manifests import canonical
from .provider_control import capture_hash, immutable_bytes


class GeminiClient:
    def __init__(self, control, api_key):
        import httpx

        self.control = control
        self._key = api_key
        register_secret(api_key)
        install_log_redaction()
        self.http = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(retries=0),
                                     timeout=120, follow_redirects=False)

    async def close(self):
        await self.http.aclose()

    async def request(self, kind, payload):
        control = self.control
        control.require_eligibility()
        model = control.policy.llm_model if kind == "llm" else control.policy.embedding_model
        method = "generateContent" if kind == "llm" else "embedContent"
        url = f"{control.policy.base_url}/models/{model}:{method}"
        rid = uuid.uuid4().hex
        directory = control.root / "requests" / rid
        # Redact before even creating the HTTP body if source/config data contains a credential.
        text = canonical(payload)
        if redact(text) != text:
            raise GeminiError("Gemini request content contains a credential; request blocked")
        request = self.http.build_request("POST", url, json=payload,
                                         headers={"x-goog-api-key": self._key})
        immutable_bytes(directory / "request.body", request.content)
        immutable_bytes(directory / "request.json", canonical({
            "method": "POST", "url": url, "provider": "gemini", "kind": kind,
            "headers": {k: redact(v) for k, v in request.headers.items()
                        if k.lower() not in ("x-goog-api-key", "authorization", "cookie")},
        }).encode())
        reserved = False
        response_hash = None
        response = None
        try:
            amount, bound = control.bounds(kind, payload)
            await control.reserve_request(rid, amount, capture_hash(directory, "request"), bound)
            reserved = True
            # A waiting request may cross the model routing deadline; check again before dispatch.
            control.require_eligibility()
            response = await self.http.send(request, stream=True)
            chunks, complete = [], False
            body, safe_body = b"", b""
            try:
                async for chunk in response.aiter_bytes():
                    chunks.append(chunk)
                complete = True
            finally:
                # The only raw bytes omitted are credential occurrences, including echoed keys.
                body = b"".join(chunks)
                safe_body = redact_bytes(body)
                immutable_bytes(directory / "response.body", safe_body)
                immutable_bytes(directory / "response.json", canonical({
                    "status": response.status_code, "body_complete": complete,
                    "credential_redacted": safe_body != body,
                    "headers": {k: redact(v) for k, v in response.headers.items()
                                if k.lower() not in ("set-cookie", "x-goog-api-key", "authorization")},
                }).encode())
                response_hash = capture_hash(directory, "response")
            if safe_body != body:
                control.freeze()
                raise GeminiError("Gemini response contained a credential; redacted capture retained and ledger frozen")
            if response.status_code == 429:
                retry = response.headers.get("retry-after", "")
                immutable_bytes(directory / "quota.json", canonical({
                    "status": 429, "retry_after_seconds": int(retry) if retry.isdigit() else None,
                    "action": "stop_no_automatic_retry_or_tier_upgrade",
                }).encode())
                control.freeze()
                raise GeminiError("Gemini quota exhausted (429); ledger frozen; inspect redacted capture")
            if not 200 <= response.status_code < 300:
                raise GeminiError(f"Gemini HTTP {response.status_code}; reservation retained; no retry")
            data = json.loads(safe_body)
            if kind == "llm":
                version = data.get("modelVersion", "")
                if not isinstance(version, str) or not re.fullmatch(r"gemini-2\.5-flash(?:-[0-9]{3})?", version):
                    control.freeze()
                    raise GeminiError("Gemini returned an unapproved model version; no silent substitution")
            cost, usage = control.measured_cost(kind, data, bound, amount)
            # Charge conservative paid-equivalent reservations if embedding usage is unavailable.
            control.settle(rid, cost, response_hash)
            return data, {"kind": kind, "provider": "gemini", "requested_model": model,
                          "model_version": data.get("modelVersion"), "audit_request_id": rid,
                          "input_bound": bound, "paid_equivalent_nanodollars": cost, **usage}
        except BaseException as error:
            # Never include raw exception objects, request objects or HTTP headers in messages.
            encoded = canonical({"type": type(error).__name__, "message": redact(str(error))}).encode()
            immutable_bytes(directory / "error.json", encoded)
            if reserved:
                control.uncertain(rid, hashlib.sha256(encoded).hexdigest(), response_hash)
            else:
                control.denied(rid, capture_hash(directory, "request"), hashlib.sha256(encoded).hexdigest())
            if not isinstance(error, Exception):
                raise
            if isinstance(error, GeminiError):
                raise GeminiError(redact(str(error))) from None
            raise GeminiError("Gemini provider/transport failure; inspect redacted immutable audit capture") from None
        finally:
            if response is not None:
                await response.aclose()


class GeminiModels:
    def __deepcopy__(self, memo):
        # LightRAG asdict() copies bound callback methods into its global config.
        # An active HTTP transport/lock must not be cloned; all callbacks share
        # this guarded client and its persistent quota ledger.
        memo[id(self)] = self
        return self

    def __init__(self, config):
        if not config.get("provider_control_file") or not config.get("provider_control_sha256"):
            raise GeminiError("Gemini requires a frozen provider-specific quota/capture policy")
        if config.get("max_retries", 0) != 0:
            raise GeminiError("Gemini smoke requires zero automatic retries")
        self.control = GeminiControl(config["provider_control_file"], config["provider_control_sha256"])
        self.control.require_eligibility()
        self.control.status()
        p = self.control.policy
        if (config["llm_model"] != p.llm_model or config["embedding_model"] != p.embedding_model
                or config["embedding_dimension"] != p.embedding_dimension
                or config.get("embedding_task_type") != p.embedding_task_type):
            raise GeminiError("Gemini model/dimension/task differs from the frozen indexing/query policy")
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise GeminiError("GEMINI_API_KEY is required; configure it in the shell or repository .env")
        self.config = config
        self.client = GeminiClient(self.control, key)
        self.usage = []

    async def llm(self, prompt, system_prompt=None, history_messages=None, **kwargs):
        contents = []
        for message in history_messages or []:
            if message.get("role") not in ("user", "assistant") or not isinstance(message.get("content"), str):
                raise GeminiError("Gemini supports only text user/assistant history")
            contents.append({"role": "model" if message["role"] == "assistant" else "user",
                             "parts": [{"text": message["content"]}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        config = {"temperature": 0, "candidateCount": 1,
                  "maxOutputTokens": self.control.policy.max_completion_tokens,
                  "thinkingConfig": {"thinkingBudget": 0, "includeThoughts": False}}
        if kwargs.get("keyword_extraction") or kwargs.get("response_format") == {"type": "json_object"}:
            config["responseMimeType"] = "application/json"
        payload = {"contents": contents, "generationConfig": config}
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        data, usage = await self.client.request("llm", payload)
        self.usage.append(usage)
        candidates = data.get("candidates") or []
        if not candidates:
            raise GeminiError("Gemini returned no candidate (blocked/empty); raw response retained")
        parts = candidates[0].get("content", {}).get("parts", [])
        usage["finish_reason"] = candidates[0].get("finishReason")
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        # Truncated/blocked returned text is not repaired; strict final parsing still records failures.
        return text

    async def embedding(self, texts, **kwargs):
        import numpy as np

        values = []
        for text in texts:
            data, usage = await self.client.request("embedding", {
                "model": "models/" + self.control.policy.embedding_model,
                "content": {"parts": [{"text": text}]},
                "taskType": self.control.policy.embedding_task_type,
                "outputDimensionality": self.control.policy.embedding_dimension,
            })
            self.usage.append(usage)
            try:
                vector = np.asarray(data["embedding"]["values"], dtype=np.float32)
            except (KeyError, TypeError, ValueError):
                raise GeminiError("Gemini returned an invalid embedding; redacted raw response retained") from None
            if vector.shape != (self.control.policy.embedding_dimension,) or not np.isfinite(vector).all():
                raise GeminiError("Gemini returned an unexpected embedding dimension or nonfinite vector")
            norm = np.linalg.norm(vector)
            if not np.isfinite(norm) or norm <= 0:
                raise GeminiError("Gemini returned a zero/invalid embedding vector")
            # Required for Embedding 001's reduced dimensions; apply identically on every callback.
            values.append(vector / norm)
        return np.asarray(values, dtype=np.float32).reshape((-1, self.control.policy.embedding_dimension))
