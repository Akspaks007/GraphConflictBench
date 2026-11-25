"""Exercise standard indexing, Local Search provenance and build recovery."""

import json
import os
from pathlib import Path

import pytest

from graphconflictbench.adapters.microsoft_graphrag_adapter import MicrosoftGraphRAGAdapter
from graphconflictbench.cli import dispatch, parser
from graphconflictbench.manifests import read_jsonl, verify_checksums

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "results/step4-validity-v2-20261115/stratified-smoke-v2"


@pytest.mark.native
@pytest.mark.skipif(
    not os.environ.get("GCB_MICROSOFT_GRAPHRAG_PYTHON"),
    reason="set GCB_MICROSOFT_GRAPHRAG_PYTHON to opt in",
)
def test_local_search_index_recovery_and_source_mapping(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    common = [
        "--arch", "microsoft_graphrag",
        "--worker-python", os.environ["GCB_MICROSOFT_GRAPHRAG_PYTHON"],
        "--dataset", str(DATASET),
    ]

    def cli(command, *args):
        return dispatch(parser().parse_args([command, *common, *args]))

    call = MicrosoftGraphRAGAdapter._call

    def interrupt(self, operation, directory, **kwargs):
        result = call(self, operation, directory, **kwargs)
        if operation == "index":
            raise RuntimeError("interrupted before committing index")
        return result

    keys = set()
    for condition in ("conflict", "control"):
        index = tmp_path / "indexes" / condition
        index_args = ("--condition", condition, "--output-dir", str(index))
        if condition == "conflict":
            with monkeypatch.context() as fault:
                fault.setattr(MicrosoftGraphRAGAdapter, "_call", interrupt)
                with pytest.raises(RuntimeError, match="interrupted before committing index"):
                    cli("index", *index_args)
        built = cli("index", *index_args, "--resume")
        assert built["status"] == "complete"
        assert built["documents_processed"] == 30
        assert cli("index", *index_args, "--resume") == built
        keys.add(built["index_key"])
        checkpoint = json.loads((index / "index_checkpoint.json").read_bytes())
        build = json.loads((index / checkpoint["batch"] / "build/response.json").read_bytes())
        assert build["table_rows"]["relationships"] > 0
        if condition == "conflict":
            assert build["model_cache_hits"] >= 30

        run = tmp_path / "runs" / condition
        args = ("--condition", condition, "--index-dir", str(index), "--output-dir", str(run))
        summary = cli("run", *args)
        assert summary["cases"] == 6
        assert summary["valid_output_rate"] == 1
        assert summary["benchmark_eligible"] is False
        assert cli("run", *args, "--resume") == summary
        verify_checksums(index, json.loads((index / "index_manifest.json").read_bytes())["checksums"])
        docs = {
            row["doc_id"]: row["text"]
            for row in read_jsonl(DATASET / f"corpora/pilot/{condition}/documents.jsonl")
        }
        for row in read_jsonl(run / "retrieval.jsonl"):
            assert row["architecture"] == "microsoft_graphrag"
            assert 0 < row["context_tokens"] <= 3072
            assert row["retrieved_items"]
            assert row["retrieved_graph_path_length"] is None
            for item in row["retrieved_items"]:
                assert item["mapping_status"] == "exact_quote"
                assert item["text"] in docs[item["doc_id"]]
                assert item["native_chunk_id"]
                assert item["native_score"] is None
            case_dir = run / "cases" / row["case_id"]
            raw = json.loads((case_dir / "native-1/response.json").read_bytes())["raw"]
            assert raw["native_result"]["sources"]
            assert raw["native_result"]["entities"]
            assert raw["native_context"]
    assert len(keys) == 2
