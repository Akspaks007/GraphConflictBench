"""Exercise both conditions through the CLI and the pinned HippoRAG 2 worker."""

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
    not os.environ.get("GCB_HIPPORAG2_PYTHON"), reason="set GCB_HIPPORAG2_PYTHON to opt in"
)
def test_hipporag2_build_retrieve_and_resume(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    common = [
        "--arch", "hipporag2", "--worker-python", os.environ["GCB_HIPPORAG2_PYTHON"],
        "--dataset", str(DATASET),
    ]

    def cli(command, *args):
        return dispatch(parser().parse_args([command, *common, *args]))

    keys = set()
    for condition in ("conflict", "control"):
        index = tmp_path / "indexes" / condition
        index_args = ("--condition", condition, "--output-dir", str(index))
        built = cli("index", *index_args)
        assert cli("index", *index_args, "--resume") == built
        keys.add(built["index_key"])
        manifest_path = index / "index_manifest.json"
        original = file_hash(manifest_path)
        manifest = json.loads(manifest_path.read_bytes())
        assert manifest["build_result"]["documents_processed"] == 30
        assert manifest["build_result"]["graph_edges"] > 0

        output = tmp_path / "runs" / condition
        run_args = ("--condition", condition, "--index-dir", str(index),
                    "--output-dir", str(output))
        summary = cli("run", *run_args)
        assert summary["cases"] == 6
        assert summary["valid_output_rate"] == 1
        assert summary["benchmark_eligible"] is False
        assert cli("run", *run_args, "--resume") == summary
        assert file_hash(manifest_path) == original
        verify_checksums(index, manifest["checksums"])

        source_ids = {
            row["doc_id"] for row in read_jsonl(DATASET / f"corpora/pilot/{condition}/documents.jsonl")
        }
        for row in read_jsonl(output / "retrieval.jsonl"):
            assert row["architecture"] == "hipporag2"
            assert row["retrieved_graph_path_length"] is None
            assert 0 < row["context_tokens"] <= 3072
            assert row["retrieved_items"]
            for item in row["retrieved_items"]:
                assert item["mapping_status"] == "exact_quote"
                assert item["doc_id"] in source_ids
                assert item["native_score"] is not None
            case_dir = output / "cases" / row["case_id"]
            raw = json.loads((case_dir / "native-1/response.json").read_bytes())["raw"]
            assert raw["native_result"]["graph_seeds"]
            evidence = json.loads(json.loads((case_dir / "prompt.json").read_bytes())["prompt"])["evidence"]
            assert all(set(item) == {"doc_id", "text", "rank"} for item in evidence["sources"])
            assert all(not rows for rows in evidence["native_graph"].values())
    assert len(keys) == 2
