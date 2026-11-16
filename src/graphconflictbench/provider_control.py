"""Fail-closed request accounting and append-only provider audit capture.

Money is integer nanodollars. One SQLite ledger is shared by every worker and
generation process. No network client is constructed by init/status/verify.
"""

import hashlib
import json
import os
import sqlite3
import uuid
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Literal

from pydantic import Field

from .manifests import canonical, digest, file_hash
from .schemas import Record


class ProviderPolicy(Record):
    base_url: Literal["https://api.openai.com/v1"] = "https://api.openai.com/v1"
    llm_model: str
    embedding_model: str
    cap_nanodollars: int = Field(gt=0, le=2_000_000_000)
    llm_input_nanodollars_per_token: int = Field(gt=0)
    llm_output_nanodollars_per_token: int = Field(gt=0)
    embedding_nanodollars_per_token: int = Field(gt=0)
    max_completion_tokens: int = Field(gt=0, le=16384)
    max_request_input_tokens: int = Field(gt=0, le=128000)
    state_directory: str


def immutable_bytes(path, data):
    """Create once, fsync, and never replace an existing audit record."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


class ProviderControl:
    def __init__(self, policy_file, expected_hash=None):
        self.policy_file = Path(policy_file).resolve()
        if expected_hash and file_hash(self.policy_file) != expected_hash:
            raise ValueError("provider policy checksum changed")
        self.policy = ProviderPolicy.model_validate_json(self.policy_file.read_bytes())
        self.identity = digest(self.policy.model_dump(mode="json"))
        self.root = (self.policy_file.parent / self.policy.state_directory).resolve()
        self.database = self.root / "ledger.sqlite3"

    def initialize(self):
        # Never initialize on an inference path, and never reset an existing ledger.
        self.root.mkdir(parents=True, exist_ok=False)
        immutable_bytes(self.root / "policy.json", canonical(self.policy.model_dump()).encode())
        with closing(sqlite3.connect(self.database)) as db, db:
            db.executescript(
                "CREATE TABLE meta (identity TEXT NOT NULL, frozen INTEGER NOT NULL);"
                "CREATE TABLE requests (id TEXT PRIMARY KEY, reserved INTEGER NOT NULL, "
                "charged INTEGER, status TEXT NOT NULL, request_hash TEXT NOT NULL, "
                "response_hash TEXT, error_hash TEXT);"
            )
            db.execute("INSERT INTO meta VALUES (?,0)", (self.identity,))
        return self.status()

    @contextmanager
    def connect(self):
        if not self.database.is_file():
            raise RuntimeError("provider ledger is not initialized; run provider-control init")
        db = sqlite3.connect(self.database, timeout=30)
        try:
            identity, _ = db.execute("SELECT identity,frozen FROM meta").fetchone()
            stored = json.loads((self.root / "policy.json").read_text())
            if identity != self.identity or digest(stored) != self.identity:
                raise ValueError("provider ledger policy identity changed")
            with db:
                yield db
        finally:
            db.close()

    def request_bound(self, endpoint, payload, body):
        p = self.policy
        if endpoint == "/v1/chat/completions":
            if set(payload) - {"model", "messages", "temperature", "max_tokens", "response_format"}:
                raise ValueError("unpriced chat request options")
            if payload.get("model") != p.llm_model:
                raise ValueError("unpriced LLM model")
            if payload.get("stream") or payload.get("n", 1) != 1 or payload.get("tools"):
                raise ValueError("streaming, multiple completions and tools are not budgeted")
            output = payload.get("max_tokens")
            if type(output) is not int or not 0 < output <= p.max_completion_tokens:
                raise ValueError("a bounded max_tokens is mandatory")
            messages = payload.get("messages")
            if not isinstance(messages, list) or not all(
                isinstance(m, dict) and isinstance(m.get("content"), str)
                and m.get("role") in ("system", "user", "assistant") for m in messages
            ):
                raise ValueError("only plain text messages are priced")
            # Byte-level BPE tokens cannot outnumber UTF-8 bytes of plain text.
            # Include the entire wire JSON plus generous message framing overhead.
            bound = len(body) + 256 * (len(messages) + 1)
            rate = p.llm_input_nanodollars_per_token
            reserved = bound * rate + output * p.llm_output_nanodollars_per_token
        elif endpoint == "/v1/embeddings":
            if set(payload) - {"model", "input", "dimensions", "encoding_format"}:
                raise ValueError("unpriced embedding request options")
            if payload.get("model") != p.embedding_model:
                raise ValueError("unpriced embedding model")
            texts = payload.get("input")
            if not isinstance(texts, list) or not texts or not all(isinstance(t, str) for t in texts):
                raise ValueError("only nonempty lists of embedding text are priced")
            bound = sum(len(t.encode("utf-8")) + 16 for t in texts)
            output = 0
            reserved = bound * p.embedding_nanodollars_per_token
        else:
            raise ValueError("unpriced provider endpoint")
        if bound > p.max_request_input_tokens:
            raise ValueError("request exceeds conservative input-token reservation limit")
        return reserved, bound, output

    def reserve(self, request_id, amount, request_hash):
        if type(amount) is not int or amount <= 0:
            raise ValueError("reservation must be positive integer nanodollars")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            frozen = db.execute("SELECT frozen FROM meta").fetchone()[0]
            total = db.execute(
                "SELECT COALESCE(SUM(COALESCE(charged,reserved)),0) FROM requests"
            ).fetchone()[0]
            if frozen or total + amount > self.policy.cap_nanodollars:
                raise RuntimeError("provider spending cap reached or ledger frozen")
            db.execute("INSERT INTO requests VALUES (?,?,NULL,'reserved',?,NULL,NULL)",
                       (request_id, amount, request_hash))

    def settle(self, request_id, amount, response_hash):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT reserved,status FROM requests WHERE id=?", (request_id,)).fetchone()
            if not row or row[1] != "reserved":
                raise RuntimeError("request already settled or unknown")
            if type(amount) is not int or amount < 0 or amount > row[0]:
                db.execute("UPDATE meta SET frozen=1")
                db.commit()
                raise RuntimeError("usage exceeded reservation; ledger frozen for reconciliation")
            db.execute("UPDATE requests SET charged=?,status='settled',response_hash=? WHERE id=?",
                       (amount, response_hash, request_id))

    def uncertain(self, request_id, error_hash, response_hash=None):
        # Unknown billing consumes the FULL reservation indefinitely; no automatic refund.
        with self.connect() as db:
            db.execute("UPDATE requests SET status='uncertain',error_hash=?,response_hash=? "
                       "WHERE id=? AND status='reserved'", (error_hash, response_hash, request_id))

    def denied(self, request_id, request_hash, error_hash):
        with self.connect() as db:
            db.execute("INSERT INTO requests VALUES (?,0,0,'denied',?,NULL,?)",
                       (request_id, request_hash, error_hash))

    def status(self):
        with self.connect() as db:
            charged, held, calls = db.execute(
                "SELECT COALESCE(SUM(charged),0),"
                "COALESCE(SUM(CASE WHEN charged IS NULL THEN reserved ELSE 0 END),0),"
                "COUNT(*) FROM requests"
            ).fetchone()
            frozen = bool(db.execute("SELECT frozen FROM meta").fetchone()[0])
            counts = dict(db.execute("SELECT status,COUNT(*) FROM requests GROUP BY status"))
        return {"cap_nanodollars": self.policy.cap_nanodollars, "charged_nanodollars": charged,
                "held_nanodollars": held, "available_nanodollars": self.policy.cap_nanodollars
                - charged - held, "requests": calls, "status_counts": counts,
                "frozen": frozen, "policy_identity": self.identity}

    def freeze(self):
        with self.connect() as db:
            db.execute("UPDATE meta SET frozen=1")

    def verify(self):
        with self.connect() as db:
            ids = {r[0] for r in db.execute("SELECT id FROM requests")}
            captured = {p.name for p in (self.root / "requests").glob("*") if p.is_dir()}
            if ids != captured:
                raise ValueError("unreconciled provider capture/ledger records")
            for rid, req, resp, err in db.execute(
                "SELECT id,request_hash,response_hash,error_hash FROM requests"
            ):
                directory = self.root / "requests" / rid
                for stem, expected in (("request", req), ("response", resp)):
                    if expected and capture_hash(directory, stem) != expected:
                        raise ValueError(f"provider audit hash mismatch: {rid}/{stem}")
                if err and file_hash(directory / "error.json") != err:
                    raise ValueError(f"provider audit hash mismatch: {rid}/error.json")
        return {**self.status(), "audit_integrity": "passed"}

    def usage_cost(self, endpoint, data, input_bound, output_bound):
        usage = data.get("usage") if isinstance(data, dict) else None
        usage = usage if isinstance(usage, dict) else {}
        inputs = usage.get("prompt_tokens")
        outputs = usage.get("completion_tokens") if endpoint.endswith("completions") else 0
        if (type(inputs) is not int or type(outputs) is not int or inputs < 0 or outputs < 0
                or inputs > input_bound or outputs > output_bound
                or ("total_tokens" in usage and usage["total_tokens"] != inputs + outputs)):
            self.freeze()
            raise RuntimeError("missing/invalid/out-of-bound provider usage; reservation retained")
        p = self.policy
        rate = (p.llm_input_nanodollars_per_token if endpoint.endswith("completions")
                else p.embedding_nanodollars_per_token)
        return inputs * rate + outputs * p.llm_output_nanodollars_per_token


def capture_hash(directory, stem):
    return digest({ext: file_hash(directory / (stem + ext)) for ext in (".body", ".json")})


def audited_http_client(control, transport=None):
    """Wrap the actual HTTP dispatch, including SDK errors; lazy optional import.

    Authentication headers are excluded. Bodies are captured byte-for-byte at
    the HTTP client boundary (response content after HTTP decompression).
    """
    import httpx

    def headers_without_credentials(headers):
        secrets = {"authorization", "proxy-authorization", "api-key", "x-api-key", "cookie", "set-cookie"}
        return {k: v for k, v in headers.items() if k.lower() not in secrets}

    class AuditedTransport(httpx.AsyncBaseTransport):
        def __init__(self):
            self.inner = transport or httpx.AsyncHTTPTransport(retries=0)

        async def handle_async_request(self, request):
            rid = uuid.uuid4().hex
            directory = control.root / "requests" / rid
            body = await request.aread()
            immutable_bytes(directory / "request.body", body)
            metadata = {"method": request.method, "url": str(request.url),
                        "headers": headers_without_credentials(request.headers)}
            immutable_bytes(directory / "request.json", canonical(metadata).encode())
            reserved = False
            response_hash = None
            try:
                if (request.method != "POST" or request.url.host != "api.openai.com"
                        or request.url.scheme != "https" or request.url.port not in (None, 443)
                        or request.url.query):
                    raise ValueError("provider origin/method is not priced")
                payload = json.loads(body)
                amount, input_bound, output_bound = control.request_bound(request.url.path, payload, body)
                control.reserve(rid, amount, capture_hash(directory, "request"))
                reserved = True
                response = await self.inner.handle_async_request(request)
                response_meta = {"status": response.status_code,
                                 "headers": headers_without_credentials(response.headers)}
                chunks = []
                complete = False
                try:
                    async for chunk in response.aiter_bytes():
                        chunks.append(chunk)
                    complete = True
                finally:
                    response_body = b"".join(chunks)
                    immutable_bytes(directory / "response.body", response_body)
                    response_meta["body_complete"] = complete
                    immutable_bytes(directory / "response.json", canonical(response_meta).encode())
                    response_hash = capture_hash(directory, "response")
                if not 200 <= response.status_code < 300:
                    raise RuntimeError(f"provider HTTP {response.status_code}; reservation retained")
                cost = control.usage_cost(request.url.path, json.loads(response_body), input_bound, output_bound)
                control.settle(rid, cost, response_hash)
                await response.aclose()
                headers = {k: v for k, v in response.headers.items()
                           if k.lower() not in ("content-encoding", "content-length", "transfer-encoding")}
                return httpx.Response(response.status_code, headers=headers,
                                      content=response_body, request=request)
            except BaseException as error:
                encoded = canonical({"type": type(error).__name__, "message": str(error)}).encode()
                immutable_bytes(directory / "error.json", encoded)
                if reserved:
                    control.uncertain(rid, hashlib.sha256(encoded).hexdigest(), response_hash)
                else:
                    control.denied(rid, capture_hash(directory, "request"),
                                   hashlib.sha256(encoded).hexdigest())
                raise

        async def aclose(self):
            await self.inner.aclose()

    return httpx.AsyncClient(transport=AuditedTransport(), timeout=120, follow_redirects=False)
