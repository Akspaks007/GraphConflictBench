"""Actual native LightRAG indexes/retrieval with Gemini REST responses doubled offline.

These are plumbing checks, never Gemini capability or free-tier findings.
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from graphconflictbench.adapters import lightrag_worker
from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter
from graphconflictbench.gemini_control import GeminiControl, GeminiPolicy
from graphconflictbench.inference import fixture_prediction
from graphconflictbench.manifests import file_hash, write_json
from graphconflictbench.models import fixture_embedding, fixture_llm
from graphconflictbench.prompts import GRAPH_FIELDS
from graphconflictbench.runner import run

httpx = pytest.importorskip("httpx")
pytest.importorskip("lightrag")
ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.native
@pytest.mark.skipif(not os.environ.get("GCB_NATIVE_PYTHON"), reason="native SDK integration is opt-in")
def test_stratified_native_indexes_and_all_gemini_callbacks_offline(tmp_path, ontology, monkeypatch):
    now = [datetime(2026, 11, 15, tzinfo=timezone.utc).timestamp()]
    monkeypatch.setattr(GeminiControl, "clock", staticmethod(lambda: now[0]))

    async def advance(self, seconds):
        now[0] += seconds
    monkeypatch.setattr(GeminiControl, "sleep", advance)
    monkeypatch.setenv("GEMINI_API_KEY", "offline-native-gemini-key-59247")
    policy_file = tmp_path / "gemini-policy.json"
    write_json(policy_file, GeminiPolicy(
        state_directory="capture", eligibility_status="free-tier-confirmed",
        eligibility_reference="offline-native-test-project", eligibility_checked_on="2026-11-15",
        quotas_reviewed=True,
    ).model_dump())
    control = GeminiControl(policy_file)
    control.initialize()
    calls = []

    async def dispatch(request):
        # Advance only a fake clock, avoiding real waiting while testing persistent rate guards.
        now[0] += 500
        payload = json.loads(request.content)
        calls.append(request.url.path)
        if request.url.path.endswith(":embedContent"):
            text = payload["content"]["parts"][0]["text"]
            vector = await fixture_embedding([text], dimension=1536)
            return httpx.Response(200, json={"embedding": {"values": vector[0].tolist()},
                                           "usageMetadata": {"promptTokenCount": 10}})
        prompt = payload["contents"][-1]["parts"][0]["text"]
        system = payload.get("systemInstruction", {}).get("parts", [{"text": ""}])[0]["text"]
        history = [{"role": "assistant" if c["role"] == "model" else "user",
                    "content": c["parts"][0]["text"]} for c in payload["contents"][:-1]]
        if prompt.startswith('{"case_id":'):
            visible = json.loads(prompt)
            case = SimpleNamespace(case_id=visible["case_id"], query=visible["question"])
            retrieval = SimpleNamespace(retrieved_items=[SimpleNamespace(**{
                "doc_id": d["doc_id"], "text": d["text"],
            }) for d in visible["evidence"]["sources"]])
            answer = fixture_prediction(case, retrieval).model_dump_json()
        else:
            answer = await fixture_llm(prompt, system_prompt=system, history_messages=history)
        return httpx.Response(200, json={
            "modelVersion": "gemini-2.5-flash", "candidates": [{"content": {"parts": [
                {"text": answer}]}, "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 2, "totalTokenCount": 12},
        })
    monkeypatch.setattr(httpx, "AsyncHTTPTransport", lambda **kw: httpx.MockTransport(dispatch))
    config = yaml.safe_load((ROOT / "configs/architectures/lightrag-gemini.yaml").read_text())
    config.update(provider_control_file=str(policy_file), provider_control_sha256=file_hash(policy_file))
    config_file = tmp_path / "gemini.yaml"
    config_file.write_text(yaml.safe_dump(config))
    adapter = LightRAGAdapter(config_file, os.environ["GCB_NATIVE_PYTHON"])

    def local_worker(operation, directory, **kwargs):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=False)
        request = {"operation": operation, "config": adapter.config, **kwargs}
        write_json(directory / "request.json", request)
        result = ({"status": "available", "native": lightrag_worker.native_metadata()}
                  if operation == "healthcheck" else asyncio.run(lightrag_worker.execute(request)))
        write_json(directory / "response.json", result)
        return result
    # Same official worker and adapter snapshot logic; HTTP mocking stays in this process.
    monkeypatch.setattr(adapter, "_call", local_worker)
    dataset = ROOT / "results/step4-validity-v2-20261115/stratified-smoke-v2"
    index_keys = []
    for condition in ("conflict", "control"):
        index = tmp_path / "indexes" / condition
        built = adapter.index(dataset / "corpora/pilot" / condition / "corpus_manifest.json", index)
        assert built["build_result"]["documents_processed"] == 30
        index_keys.append(built["index_key"])
        before = file_hash(index / "index_manifest.json")
        output = tmp_path / "runs" / condition
        summary = run(adapter, dataset, ontology, "pilot", condition, index, output,
                      ROOT / "configs/prompts/shared_generation.txt")
        assert summary["cases"] == 6 and summary["valid_output_rate"] == 1
        assert summary["benchmark_eligible"] is False
        assert file_hash(index / "index_manifest.json") == before
        for prompt_file in (output / "cases").glob("*/prompt.json"):
            prompt = json.loads(json.loads(prompt_file.read_text())["prompt"])
            for kind, graph_rows in prompt["evidence"]["native_graph"].items():
                assert all(set(row) <= set(GRAPH_FIELDS[kind]) for row in graph_rows)
            assert "created_at" not in json.dumps(prompt)
    assert len(set(index_keys)) == 2
    assert any(p.endswith(":generateContent") for p in calls)
    assert any(p.endswith(":embedContent") for p in calls)
    status = control.verify()
    assert status["dispatched_or_reserved_requests"] == len(calls)
    assert status["held_nanodollars"] == 0
