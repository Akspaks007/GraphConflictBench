"""Gemini-only quota and paid-equivalent upper-bound accounting.

The OpenAI policy, wrapper and transport are not changed by this provider.
Project eligibility is a required human attestation, not inferred from a key.
"""

import asyncio
import json
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import ConfigDict, Field

from .environment import redact
from .manifests import digest, file_hash
from .provider_control import ProviderControl
from .schemas import Record


class GeminiError(RuntimeError):
    """Credential-safe error messages; raw replies are retained after redaction."""


class GeminiPolicy(Record):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    provider: Literal["gemini"] = "gemini"
    base_url: Literal["https://generativelanguage.googleapis.com/v1beta"] = (
        "https://generativelanguage.googleapis.com/v1beta"
    )
    llm_model: Literal["gemini-2.5-flash"] = "gemini-2.5-flash"
    embedding_model: Literal["gemini-embedding-001"] = "gemini-embedding-001"
    embedding_dimension: Literal[768, 1536, 3072] = 1536
    embedding_task_type: Literal["SEMANTIC_SIMILARITY"] = "SEMANTIC_SIMILARITY"
    eligibility_status: Literal["unverified", "free-tier-confirmed", "paid-tier-confirmed"] = "unverified"
    eligibility_reference: str = ""
    eligibility_checked_on: str = ""
    quotas_reviewed: bool = False
    # December 1 automatic rerouting is an experimental identity change, not a fallback.
    not_after: Literal["2026-12-01"] = "2026-12-01"
    cap_nanodollars: int = Field(default=2_000_000_000, gt=0, le=2_000_000_000)
    # Standard Gemini 2.5 Flash / Embedding 001 prices, NOT OpenAI prices.
    # Reserve these even after free-tier confirmation: actual billing is not observable here.
    llm_input_nanodollars_per_token: Literal[300] = 300
    llm_output_nanodollars_per_token: Literal[2500] = 2500
    embedding_nanodollars_per_token: Literal[150] = 150
    max_completion_tokens: int = Field(default=1536, gt=0, le=1536)
    max_request_input_tokens: int = Field(default=32768, gt=0, le=32768)
    max_requests: int = Field(default=500, gt=0, le=500)
    max_requests_per_24h: int = Field(default=200, gt=0, le=200)
    min_interval_seconds: int = Field(default=31, ge=31)
    max_input_tokens_per_minute: int = Field(default=40000, gt=0, le=40000)
    state_directory: str


class GeminiControl(ProviderControl):
    clock = staticmethod(time.time)

    def __init__(self, policy_file, expected_hash=None):
        self.policy_file = Path(policy_file).resolve()
        if expected_hash and file_hash(self.policy_file) != expected_hash:
            raise ValueError("Gemini policy checksum changed")
        text = self.policy_file.read_text(encoding="utf-8")
        if redact(text) != text:
            raise GeminiError("Gemini policy must not contain a credential")
        self.policy = GeminiPolicy.model_validate_json(text)
        self.identity = digest(self.policy.model_dump(mode="json"))
        self.root = (self.policy_file.parent / self.policy.state_directory).resolve()
        self.database = self.root / "ledger.sqlite3"

    def require_eligibility(self):
        p = self.policy
        today = datetime.fromtimestamp(self.clock(), timezone.utc).date()
        if today >= date.fromisoformat(p.not_after):
            raise GeminiError("Gemini 2.5 Flash routing deadline reached; review a replacement explicitly")
        if (p.eligibility_status == "unverified" or not p.eligibility_reference.strip()
                or not p.quotas_reviewed):
            raise GeminiError("Gemini project/model tier eligibility and active quotas need human verification")
        try:
            checked = date.fromisoformat(p.eligibility_checked_on)
        except ValueError:
            raise GeminiError("Gemini eligibility attestation needs a valid date") from None
        if not 0 <= (today - checked).days <= 7:
            raise GeminiError("Gemini eligibility/quota attestation is stale or future-dated")

    def initialize(self):
        self.require_eligibility()
        super().initialize()
        with self.connect() as db:
            db.execute("CREATE TABLE gemini_quota (id TEXT PRIMARY KEY, at REAL NOT NULL, "
                       "input_bound INTEGER NOT NULL)")
        return self.status()

    def status(self):
        status = super().status()
        with self.connect() as db:
            ready = bool(db.execute("SELECT name FROM sqlite_master WHERE name='gemini_quota'").fetchone())
            count = db.execute("SELECT COUNT(*) FROM gemini_quota").fetchone()[0] if ready else 0
            daily = db.execute("SELECT COUNT(*) FROM gemini_quota WHERE at>?",
                               (self.clock() - 86400,)).fetchone()[0] if ready else 0
            minute = db.execute("SELECT COALESCE(SUM(input_bound),0) FROM gemini_quota WHERE at>?",
                                (self.clock() - 60,)).fetchone()[0] if ready else 0
        return {**status, "provider": "gemini", "quota_table_ready": ready,
                "dispatched_or_reserved_requests": count, "max_requests": self.policy.max_requests,
                "requests_in_rolling_24h": daily,
                "max_requests_per_24h": self.policy.max_requests_per_24h,
                "input_bound_in_last_60s": minute,
                "max_input_tokens_per_minute": self.policy.max_input_tokens_per_minute,
                "min_interval_seconds": self.policy.min_interval_seconds,
                "eligibility_status": self.policy.eligibility_status,
                "cost_basis": "paid_equivalent_upper_bound_not_an_invoice",
                "actual_project_billing_verified_by_api": False}

    async def sleep(self, seconds):
        await asyncio.sleep(seconds)

    def try_reserve(self, rid, amount, request_hash, input_bound):
        """One transaction covers cost, lifetime/24h count, TPM and dispatch spacing."""
        self.require_eligibility()
        now = self.clock()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT frozen FROM meta").fetchone()[0]:
                raise GeminiError("Gemini ledger frozen; inspect captured error/quota evidence")
            count, latest = db.execute("SELECT COUNT(*),MAX(at) FROM gemini_quota").fetchone()
            if count >= self.policy.max_requests:
                raise GeminiError("Gemini conservative total request limit reached")
            daily = db.execute("SELECT COUNT(*) FROM gemini_quota WHERE at>?", (now - 86400,)).fetchone()[0]
            if daily >= self.policy.max_requests_per_24h:
                raise GeminiError("Gemini rolling-24h request cap reached; do not restart the ledger")
            if input_bound > self.policy.max_input_tokens_per_minute:
                raise GeminiError("Gemini request exceeds the conservative input TPM bound")
            recent = list(db.execute("SELECT at,input_bound FROM gemini_quota WHERE at>? ORDER BY at",
                                     (now - 60,)))
            wait = max(0, (latest or 0) + self.policy.min_interval_seconds - now)
            total = sum(x[1] for x in recent)
            for at, bound in recent:
                if total + input_bound <= self.policy.max_input_tokens_per_minute:
                    break
                wait = max(wait, at + 60.01 - now)
                total -= bound
            if wait > 0:
                return wait
            committed = db.execute("SELECT COALESCE(SUM(COALESCE(charged,reserved)),0) FROM requests").fetchone()[0]
            if committed + amount > self.policy.cap_nanodollars:
                raise GeminiError("Gemini paid-equivalent reservation cap reached")
            db.execute("INSERT INTO requests VALUES (?,?,NULL,'reserved',?,NULL,NULL)", (rid, amount, request_hash))
            db.execute("INSERT INTO gemini_quota VALUES (?,?,?)", (rid, now, input_bound))
        return 0

    async def reserve_request(self, rid, amount, request_hash, input_bound):
        while True:
            wait = self.try_reserve(rid, amount, request_hash, input_bound)
            if wait == 0:
                return
            await self.sleep(wait)

    def bounds(self, kind, payload):
        p = self.policy
        def text_only(content):
            return (isinstance(content, dict) and set(content) <= {"role", "parts"}
                    and content.get("role", "user") in ("user", "model")
                    and isinstance(content.get("parts"), list) and bool(content["parts"])
                    and all(isinstance(part, dict) and set(part) == {"text"}
                            and isinstance(part["text"], str) for part in content["parts"]))

        if kind == "llm":
            if (set(payload) - {"contents", "generationConfig", "systemInstruction"}
                    or not isinstance(payload.get("contents"), list) or not payload["contents"]
                    or not all(text_only(c) for c in payload["contents"])
                    or ("systemInstruction" in payload and not text_only(payload["systemInstruction"]))):
                raise GeminiError("Gemini permits only reviewed text generation requests")
            config = payload["generationConfig"]
            if (not isinstance(config, dict) or set(config) - {
                    "temperature", "candidateCount", "maxOutputTokens", "thinkingConfig", "responseMimeType"}
                    or config.get("candidateCount") != 1 or config.get("temperature") != 0
                    or config.get("responseMimeType", "application/json") != "application/json"
                    or config["maxOutputTokens"] != p.max_completion_tokens
                    or config["thinkingConfig"] != {"thinkingBudget": 0, "includeThoughts": False}):
                raise GeminiError("Gemini output/thinking limits differ from the frozen policy")
            # Conservative plain-text reservation, not an assertion about Google's billing tokenizer.
            bound = len(json.dumps(payload, ensure_ascii=False).encode()) + 1024 * (len(payload["contents"]) + 1)
            amount = bound * p.llm_input_nanodollars_per_token + p.max_completion_tokens * p.llm_output_nanodollars_per_token
        elif kind == "embedding":
            if (set(payload) != {"model", "content", "outputDimensionality", "taskType"}
                    or not text_only(payload["content"]) or len(payload["content"]["parts"]) != 1
                    or payload["model"] != "models/" + p.embedding_model
                    or payload["outputDimensionality"] != p.embedding_dimension
                    or payload["taskType"] != p.embedding_task_type):
                raise GeminiError("Gemini embedding space differs from the frozen policy")
            text = payload["content"]["parts"][0]["text"]
            bound = len(text.encode()) + 16
            if bound > 2048:
                raise GeminiError("Gemini embedding exceeds conservative 2048-token byte bound; no truncation")
            amount = bound * p.embedding_nanodollars_per_token
        else:
            raise GeminiError("unpriced Gemini request kind")
        if bound > p.max_request_input_tokens:
            raise GeminiError("Gemini request exceeds conservative input bound")
        return amount, bound

    def measured_cost(self, kind, data, bound, reservation):
        usage = data.get("usageMetadata")
        if kind == "embedding" and not usage:
            return reservation, {"source": "upper_bound_no_usage_metadata", "provider_usage": None}
        if not isinstance(usage, dict):
            self.freeze()
            raise GeminiError("Gemini usage is missing; ledger frozen and reservation retained")
        inputs = usage.get("promptTokenCount")
        outputs = usage.get("candidatesTokenCount") if kind == "llm" else 0
        thoughts = usage.get("thoughtsTokenCount", 0)
        if (type(inputs) is not int or inputs < 0 or inputs > bound
                or type(outputs) is not int or outputs < 0
                or outputs > self.policy.max_completion_tokens
                or type(thoughts) is not int or thoughts != 0):
            self.freeze()
            raise GeminiError("Gemini usage/thinking exceeds policy bounds; reservation retained")
        if kind == "llm":
            total = usage.get("totalTokenCount")
            if type(total) is not int or total != inputs + outputs:
                self.freeze()
                raise GeminiError("Gemini usage totals are inconsistent; reservation retained")
        rate = (self.policy.llm_input_nanodollars_per_token if kind == "llm"
                else self.policy.embedding_nanodollars_per_token)
        return inputs * rate + outputs * self.policy.llm_output_nanodollars_per_token, {
            "source": "provider_usage_at_paid_equivalent_rates", "provider_usage": usage,
        }
