"""Offline HTTP/SDK doubles. No real provider endpoint is ever dispatched."""

import asyncio
import json

import pytest

from graphconflictbench.groq_models import GroqModels
from graphconflictbench.manifests import file_hash
from graphconflictbench.models import OpenAIModels
from graphconflictbench.provider_control import ProviderControl, audited_http_client

httpx = pytest.importorskip("httpx")
pytest.importorskip("openai")


@pytest.fixture
def control(tmp_path):
    policy = tmp_path / "policy.json"
    policy.write_text(json.dumps({
        "llm_model": "gpt-4o-mini-2024-07-18", "embedding_model": "text-embedding-3-small",
        "cap_nanodollars": 2_000_000_000, "llm_input_nanodollars_per_token": 150,
        "llm_output_nanodollars_per_token": 600, "embedding_nanodollars_per_token": 20,
        "max_completion_tokens": 1536, "max_request_input_tokens": 128000,
        "state_directory": "ledger",
    }))
    guard = ProviderControl(policy)
    guard.initialize()
    return guard


def completion(control, **updates):
    return {"model": control.policy.llm_model, "max_tokens": 100,
            "messages": [{"role": "user", "content": "text"}], **updates}


@pytest.mark.parametrize(("rotate", "pace"), [(False, False), (True, False), (False, True)])
def test_groq_sdk_dispatch_and_local_embedding(control, monkeypatch, rotate, pace):
    import numpy as np

    policy = control.policy.model_dump()
    policy.update(base_url=GroqModels.base_url, llm_model="openai/gpt-oss-20b",
                  embedding_model="BAAI/bge-small-en-v1.5", embedding_nanodollars_per_token=0,
                  state_directory="groq-ledger")
    control.policy_file.write_text(json.dumps(policy))
    control = ProviderControl(control.policy_file)
    control.initialize()
    dispatched = []

    def dispatch(request):
        assert str(request.url) == f"{GroqModels.base_url}/chat/completions"
        dispatched.append(request.headers["authorization"])
        body = json.loads(request.content)
        assert body["max_completion_tokens"] == policy["max_completion_tokens"]
        assert body["reasoning_effort"] == "low"
        assert body["response_format"] == {"type": "json_object"}
        return httpx.Response(200, json={
            "id": "offline", "object": "chat.completion", "created": 0, "model": body["model"],
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "{}"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
        })

    class LocalEmbedding:
        def embed(self, texts):
            return (np.ones(384) for _ in texts)

    monkeypatch.setenv("GROQ_API_KEY", "offline-groq-key")
    monkeypatch.delenv("GROQ_API_KEYS", raising=False)
    monkeypatch.delenv("GCB_GROQ_MIN_KEY_INTERVAL_SECONDS", raising=False)
    delays = []
    if pace:
        async def capture_delay(seconds):
            delays.append(seconds)

        monkeypatch.setenv("GCB_GROQ_MIN_KEY_INTERVAL_SECONDS", "30")
        monkeypatch.setattr(asyncio, "sleep", capture_delay)
    if rotate:
        monkeypatch.setenv(
            "GROQ_API_KEYS", "offline-first, offline-second, offline-third, offline-first"
        )
    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **kw: httpx.MockTransport(dispatch))
    config = {**policy, "provider_control_file": str(control.policy_file),
              "provider_control_sha256": file_hash(control.policy_file), "embedding_dimension": 384}

    async def invoke():
        models = GroqModels(config)
        models.local_embedding = LocalEmbedding()
        async with models.client:
            assert await models.llm("Return a JSON object", keyword_extraction=True) == "{}"
            assert (await models.embedding(["Text"])).shape == (1, 384)
        # A new client reads the shared sequence instead of starting with key one.
        models = GroqModels(config)
        async with models.client:
            for _ in range(3):
                assert await models.llm("Return a JSON object", keyword_extraction=True) == "{}"

    asyncio.run(invoke())
    expected = ["offline-first", "offline-second", "offline-third", "offline-first"] if rotate else [
        "offline-groq-key"
    ] * 4
    assert dispatched == [f"Bearer {key}" for key in expected]
    if pace:
        assert len(delays) == 3 and 0 < delays[0] <= 30
    status = control.verify()
    assert status["requests"] == 4
    assert status["charged_nanodollars"] == 4 * 2700
    for request in (control.root / "requests").glob("*/request.json"):
        assert "authorization" not in json.loads(request.read_text())["headers"]
        assert all(key not in request.read_text() for key in expected)


def test_actual_sdk_callbacks_capture_every_stage_in_shared_ledger(control, monkeypatch):
    calls = []

    def dispatch(request):
        body = json.loads(request.content)
        calls.append(body)
        if request.url.path == "/v1/embeddings":
            return httpx.Response(200, json={
                "object": "list", "model": body["model"],
                "data": [{"object": "embedding", "index": 0, "embedding": [0.2, 0.3]}],
                "usage": {"prompt_tokens": 10, "total_tokens": 10},
            })
        return httpx.Response(200, headers={"x-request-id": "offline-request"}, json={
            "id": "offline", "object": "chat.completion", "created": 0, "model": body["model"],
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "{}"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
        })

    monkeypatch.setenv("OPENAI_API_KEY", "OFFLINE_SECRET_NEVER_A_REAL_KEY")
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **kw: httpx.MockTransport(dispatch))
    config = {"provider_control_file": str(control.policy_file),
              "provider_control_sha256": file_hash(control.policy_file), "max_retries": 0,
              "llm_model": control.policy.llm_model, "embedding_model": control.policy.embedding_model,
              "embedding_dimension": 2}

    async def invoke():
        # Worker instances and separate final generators all point at the same policy/ledger.
        worker = OpenAIModels(config)
        generator = OpenAIModels(config)
        try:
            await worker.llm("extract source")
            await worker.llm("glean", history_messages=[{"role": "assistant", "content": "{}"}])
            await worker.llm("summarize descriptions")
            await worker.llm("keywords", response_format={"type": "json_object"})
            values = await worker.embedding(["source / entity / relationship / retrieval query"])
            assert values.shape == (1, 2)
            await generator.llm("final generation")
        finally:
            await worker.client.close()
            await generator.client.close()
    asyncio.run(invoke())
    assert len(calls) == 6
    assert control.verify()["requests"] == 6
    assert control.status()["held_nanodollars"] == 0
    assert control.status()["charged_nanodollars"] == 5 * 2700 + 200
    assert all(c["max_tokens"] == 1536 for c in calls if "messages" in c)
    assert calls[3]["response_format"] == {"type": "json_object"}
    for directory in (control.root / "requests").iterdir():
        assert (directory / "response.body").is_file()
        assert "OFFLINE_SECRET" not in (directory / "request.json").read_text()
        assert "authorization" not in json.loads((directory / "request.json").read_text())["headers"]
    directory = next((control.root / "requests").iterdir())
    (directory / "request.json").write_text("{}")
    with pytest.raises(ValueError, match="hash mismatch"):
        control.verify()


@pytest.mark.parametrize("failure", ["http_error", "connection", "missing_usage", "partial_body"])
def test_failures_capture_raw_evidence_and_keep_reservations(control, failure):
    class Partial(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b'{"partial":'
            raise httpx.ReadError("offline body interruption")

    def dispatch(request):
        if failure == "connection":
            raise httpx.ConnectError("offline connection failure", request=request)
        if failure == "http_error":
            return httpx.Response(429, content=b'{"error":"offline rate limit"}')
        if failure == "partial_body":
            return httpx.Response(200, stream=Partial())
        return httpx.Response(200, content=b'{"choices":[]}')

    async def invoke():
        async with audited_http_client(control, httpx.MockTransport(dispatch)) as client:
            with pytest.raises((RuntimeError, httpx.ConnectError, httpx.ReadError)):
                await client.post("https://api.openai.com/v1/chat/completions", json=completion(control))
    asyncio.run(invoke())
    status = control.verify()
    assert status["requests"] == 1 and status["held_nanodollars"] > 0
    assert status["charged_nanodollars"] == 0
    directory = next((control.root / "requests").iterdir())
    assert (directory / "request.body").is_file() and (directory / "error.json").is_file()
    if failure != "connection":
        assert (directory / "response.body").is_file()
    if failure == "partial_body":
        assert (directory / "response.body").read_bytes() == b'{"partial":'
        assert json.loads((directory / "response.json").read_text())["body_complete"] is False
    if failure == "missing_usage":
        assert status["frozen"]


def test_exhausted_budget_and_unknown_origin_never_dispatch(control):
    control.reserve("preexisting-crashed-request", control.policy.cap_nanodollars, "pending")
    dispatched = []

    def forbidden(request):
        dispatched.append(request)
        raise AssertionError("must not reach provider")

    async def invoke():
        async with audited_http_client(control, httpx.MockTransport(forbidden)) as client:
            with pytest.raises(RuntimeError, match="spending cap"):
                await client.post("https://api.openai.com/v1/chat/completions", json=completion(control))
            with pytest.raises(ValueError, match="origin"):
                await client.post("https://unpriced.example/v1/chat/completions", json=completion(control))
    asyncio.run(invoke())
    assert not dispatched
    assert control.status()["held_nanodollars"] == control.policy.cap_nanodollars


def test_response_usage_exceeding_bound_freezes_and_keeps_capture(control):
    def dispatch(request):
        return httpx.Response(200, json={"usage": {"prompt_tokens": 1, "completion_tokens": 10000}})
    async def invoke():
        async with audited_http_client(control, httpx.MockTransport(dispatch)) as client:
            with pytest.raises(RuntimeError, match="usage"):
                await client.post("https://api.openai.com/v1/chat/completions", json=completion(control))
    asyncio.run(invoke())
    assert control.verify()["frozen"]
    assert control.status()["held_nanodollars"] > 0


def test_sdk_transport_error_is_captured_without_hidden_retries(control, monkeypatch):
    calls = []

    def dispatch(request):
        calls.append(request)
        return httpx.Response(500, content=b'{"error":"offline server error"}')

    monkeypatch.setenv("OPENAI_API_KEY", "OFFLINE_FAKE_KEY")
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **kw: httpx.MockTransport(dispatch))
    config = {"provider_control_file": str(control.policy_file),
              "provider_control_sha256": file_hash(control.policy_file), "max_retries": 0,
              "llm_model": control.policy.llm_model, "embedding_model": control.policy.embedding_model}

    async def invoke():
        models = OpenAIModels(config)
        try:
            with pytest.raises(RuntimeError, match="provider HTTP 500"):
                await models.llm("offline error")
        finally:
            await models.client.close()
    asyncio.run(invoke())
    assert len(calls) == 1 and control.verify()["held_nanodollars"] > 0
