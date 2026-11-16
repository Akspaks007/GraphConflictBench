"""Gemini REST/HTTP doubles only; no live endpoint is contacted."""

import asyncio
import copy
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from graphconflictbench import cli
from graphconflictbench.environment import load_environment
from graphconflictbench.gemini_control import GeminiControl, GeminiError, GeminiPolicy
from graphconflictbench.gemini_models import GeminiModels
from graphconflictbench.manifests import file_hash, write_json

httpx = pytest.importorskip("httpx")
np = pytest.importorskip("numpy")
ROOT = Path(__file__).resolve().parents[2]
KEY = "offline-gemini-credential-763920"


@pytest.fixture
def setup(tmp_path, monkeypatch):
    now = [datetime(2026, 11, 15, tzinfo=timezone.utc).timestamp()]
    monkeypatch.setattr(GeminiControl, "clock", staticmethod(lambda: now[0]))

    async def advance(self, seconds):
        now[0] += seconds
    monkeypatch.setattr(GeminiControl, "sleep", advance)
    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    policy = GeminiPolicy(state_directory="state", eligibility_status="free-tier-confirmed",
                          eligibility_reference="offline-project-attestation", quotas_reviewed=True,
                          eligibility_checked_on="2026-11-15")
    path = tmp_path / "policy.json"
    write_json(path, policy.model_dump())
    control = GeminiControl(path)
    control.initialize()
    config = yaml.safe_load((ROOT / "configs/architectures/lightrag-gemini.yaml").read_text())
    config.update(provider_control_file=str(path), provider_control_sha256=file_hash(path))
    return control, config, now


def generation(text="OK", **updates):
    return {"modelVersion": "gemini-2.5-flash", "candidates": [{
        "content": {"parts": [{"text": text}]}, "finishReason": "STOP"}],
        "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 2, "totalTokenCount": 12},
        **updates}


def mock_transport(monkeypatch, dispatch):
    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **kw: httpx.MockTransport(dispatch))


def test_generation_embedding_usage_and_secret_safe_capture(setup, monkeypatch):
    control, config, now = setup
    calls = []

    def dispatch(request):
        assert request.headers["x-goog-api-key"] == KEY
        assert not request.url.query
        body = json.loads(request.content)
        calls.append(body)
        if request.url.path.endswith(":embedContent"):
            assert body["outputDimensionality"] == 1536
            assert body["taskType"] == "SEMANTIC_SIMILARITY"
            return httpx.Response(200, json={"embedding": {"values": [1.0] * 1536}})
        return httpx.Response(200, json=generation())
    mock_transport(monkeypatch, dispatch)

    async def invoke():
        models = GeminiModels(config)
        try:
            assert copy.deepcopy(models) is models
            assert await models.llm("keywords", system_prompt="shared rules",
                                    history_messages=[{"role": "assistant", "content": "earlier"}],
                                    response_format={"type": "json_object"}) == "OK"
            vector = await models.embedding(["document", "retrieval query"])
            assert vector.shape == (2, 1536)
            assert np.allclose(np.linalg.norm(vector, axis=1), 1)
            assert models.usage[0]["source"] == "provider_usage_at_paid_equivalent_rates"
            assert models.usage[1]["provider_usage"] is None
        finally:
            await models.client.close()
    asyncio.run(invoke())
    assert len(calls) == 3
    assert calls[0]["contents"][0]["role"] == "model"
    assert calls[0]["systemInstruction"]["parts"][0]["text"] == "shared rules"
    assert calls[0]["generationConfig"]["responseMimeType"] == "application/json"
    assert calls[0]["generationConfig"]["thinkingConfig"]["thinkingBudget"] == 0
    assert control.verify()["requests"] == 3
    assert control.status()["charged_nanodollars"] > 8000  # Embeddings are never assumed free.
    for path in (control.root / "requests").rglob("*"):
        if path.is_file():
            assert KEY.encode() not in path.read_bytes()


@pytest.mark.parametrize("failure", ["quota", "http", "network", "echoed_key", "usage", "rerouted", "partial"])
def test_errors_are_captured_without_retries_or_secret_exposure(setup, monkeypatch, failure):
    control, config, now = setup
    calls = []

    class Partial(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b'{"partial":'
            raise httpx.ReadError("partial " + KEY)

    def dispatch(request):
        calls.append(request)
        if failure == "quota":
            return httpx.Response(429, headers={"retry-after": "60"}, json={"error": {"message": KEY}})
        if failure == "http":
            return httpx.Response(503, json={"error": "offline"})
        if failure == "network":
            raise httpx.ConnectError("connection failed " + KEY, request=request)
        if failure == "echoed_key":
            return httpx.Response(200, json=generation(text=KEY))
        if failure == "rerouted":
            return httpx.Response(200, json=generation(modelVersion="gemini-3.5-flash-lite"))
        if failure == "usage":
            return httpx.Response(200, json=generation(usageMetadata={}))
        return httpx.Response(200, stream=Partial())
    mock_transport(monkeypatch, dispatch)

    async def invoke():
        models = GeminiModels(config)
        try:
            with pytest.raises(GeminiError) as caught:
                await models.llm("offline failure")
            assert KEY not in str(caught.value)
        finally:
            await models.client.close()
    asyncio.run(invoke())
    assert len(calls) == 1
    assert control.verify()["held_nanodollars"] > 0
    for path in (control.root / "requests").rglob("*"):
        if path.is_file():
            assert KEY.encode() not in path.read_bytes()
    if failure in ("quota", "echoed_key", "usage", "rerouted"):
        assert control.status()["frozen"]
    if failure == "partial":
        path = next((control.root / "requests").glob("*/response.body"))
        assert path.read_bytes() == b'{"partial":'


def test_quota_429_retry_after_is_preserved_and_no_second_dispatch(setup, monkeypatch):
    control, config, now = setup
    calls = []

    def dispatch(request):
        calls.append(request)
        return httpx.Response(429, headers={"retry-after": "45"}, json={"error": {"code": 429}})
    mock_transport(monkeypatch, dispatch)

    async def invoke():
        models = GeminiModels(config)
        try:
            for _ in range(2):
                with pytest.raises(GeminiError):
                    await models.llm("quota")
        finally:
            await models.client.close()
    asyncio.run(invoke())
    assert len(calls) == 1
    quota = json.loads(next((control.root / "requests").glob("*/quota.json")).read_text())
    assert quota["retry_after_seconds"] == 45
    assert control.verify()["frozen"]


@pytest.mark.parametrize("values", [[1.0] * 768, ["nan"] * 1536, [0.0] * 1536])
def test_embedding_shape_finiteness_and_nonzero_norm_are_required(setup, monkeypatch, values):
    control, config, now = setup
    mock_transport(monkeypatch, lambda request: httpx.Response(200, json={"embedding": {"values": values}}))

    async def invoke():
        models = GeminiModels(config)
        try:
            with pytest.raises(GeminiError):
                await models.embedding(["text"])
        finally:
            await models.client.close()
    asyncio.run(invoke())
    assert control.verify()["requests"] == 1


def test_single_connectivity_command_is_exactly_one_request(setup, monkeypatch, tmp_path):
    control, config, now = setup
    calls = []

    def dispatch(request):
        calls.append(request)
        return httpx.Response(200, json=generation())
    mock_transport(monkeypatch, dispatch)
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config))
    result = cli.gemini_connectivity(path, tmp_path / "connectivity")
    assert result["requests"] == len(calls) == 1
    assert result["benchmark_eligible"] is False
    assert control.verify()["requests"] == 1
    with pytest.raises(FileExistsError):
        cli.gemini_connectivity(path, tmp_path / "connectivity")
    assert len(calls) == 1


def test_error_logging_redacts_echoed_secret(setup, monkeypatch, tmp_path, capsys):
    control, config, now = setup
    mock_transport(monkeypatch, lambda request: httpx.Response(200, json=generation(text=KEY)))
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config))
    dotenv = tmp_path / ".env"
    dotenv.write_text("GEMINI_API_KEY=" + KEY + "\n")
    monkeypatch.setattr(cli, "load_environment", lambda: load_environment(dotenv))
    monkeypatch.setattr("sys.argv", ["gcb", "gemini-check", "--config", str(path),
                                    "--output-dir", str(tmp_path / "check")])
    assert cli.main() == 1
    captured = capsys.readouterr()
    assert KEY not in captured.out + captured.err
    assert KEY not in (tmp_path / "check/error.json").read_text()
