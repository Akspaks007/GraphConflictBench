"""Exercise the pinned PathRAG worker, checkpoints and exact source attribution."""

import json
import os
from pathlib import Path

import pytest

from graphconflictbench.cli import dispatch, parser
from graphconflictbench.manifests import file_hash, read_jsonl, verify_checksums

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "results/step4-validity-v2-20261115/stratified-smoke-v2"


@pytest.mark.native
@pytest.mark.skipif(
    not os.environ.get("GCB_PATHRAG_PYTHON"), reason="set GCB_PATHRAG_PYTHON to opt in"
)
def test_pathrag_build_retrieve_and_resume(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    common = [
        "--arch", "pathrag", "--worker-python", os.environ["GCB_PATHRAG_PYTHON"],
        "--dataset", str(DATASET),
    ]

    def cli(command, *args):
        return dispatch(parser().parse_args([command, *common, *args]))

    keys = set()
    for condition in ("conflict", "control"):
        index = tmp_path / "indexes" / condition
        index_args = ("--condition", condition, "--output-dir", str(index), "--batch-size", "15")
        checkpoint = cli("index", *index_args)
        assert checkpoint["status"] == "partial"
        assert checkpoint["documents_processed"] == 15
        built = cli("index", *index_args, "--resume")
        assert built["status"] == "complete"
        assert built["documents_processed"] == 30
        assert cli("index", *index_args, "--resume") == built
        keys.add(built["index_key"])

        manifest_path = index / "index_manifest.json"
        original = file_hash(manifest_path)
        manifest = json.loads(manifest_path.read_bytes())
        source_docs = {
            row["doc_id"]: row["text"]
            for row in read_jsonl(DATASET / f"corpora/pilot/{condition}/documents.jsonl")
        }
        mapping = json.loads((index / "native/benchmark_sources.json").read_bytes())
        assert set(mapping.values()) == {f"{doc_id}.txt" for doc_id in source_docs}

        output = tmp_path / "runs" / condition
        run_args = ("--condition", condition, "--index-dir", str(index), "--output-dir", str(output))
        summary = cli("run", *run_args)
        assert summary["cases"] == 6
        assert summary["valid_output_rate"] == 1
        assert summary["benchmark_eligible"] is False
        assert cli("run", *run_args, "--resume") == summary
        assert file_hash(manifest_path) == original
        verify_checksums(index, manifest["checksums"])

        for row in read_jsonl(output / "retrieval.jsonl"):
            assert row["architecture"] == "pathrag"
            assert row["retrieved_graph_path_length"] is None
            assert 0 < row["context_tokens"] <= 3072
            assert row["retrieved_items"]
            for item in row["retrieved_items"]:
                assert item["mapping_status"] == "exact_quote"
                assert item["text"] in source_docs[item["doc_id"]]
                assert item["native_chunk_id"].startswith("chunk-")
                assert item["native_score"] is None
            case_dir = output / "cases" / row["case_id"]
            raw = json.loads((case_dir / "native-1/response.json").read_bytes())["raw"]
            assert "-----Sources-----" in raw["native_result"]
            assert raw["data"]["entities"]
            assert raw["data"]["relationships"]
            prompt = json.loads((case_dir / "prompt.json").read_bytes())["prompt"]
            assert all(set(item) == {"doc_id", "text", "rank"} for item in
                       json.loads(prompt)["evidence"]["sources"])
    assert len(keys) == 2
