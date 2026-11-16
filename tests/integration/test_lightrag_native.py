"""Opt-in real native SDK smoke; fixture models make no remote inference calls."""

import json
import os
from pathlib import Path

import pytest

from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter
from graphconflictbench.generator import save_dataset
from graphconflictbench.manifests import file_hash, read_jsonl
from graphconflictbench.prompts import GRAPH_FIELDS
from graphconflictbench.runner import run

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.native
@pytest.mark.skipif(
    not os.environ.get("GCB_NATIVE_PYTHON"), reason="set GCB_NATIVE_PYTHON to opt in"
)
def test_two_native_indexes_and_twelve_queries(tmp_path, ontology):
    dataset = tmp_path / "dataset"
    save_dataset(dataset, ontology, families=6)
    adapter = LightRAGAdapter(
        ROOT / "configs/architectures/lightrag-fixture.yaml", os.environ["GCB_NATIVE_PYTHON"]
    )
    keys = []
    for condition in ("conflict", "control"):
        index = tmp_path / "indexes" / condition
        corpus = dataset / "corpora/pilot" / condition / "corpus_manifest.json"
        built = adapter.index(corpus, index)
        assert built["build_result"]["documents_processed"] == 30
        assert adapter.index(corpus, index, resume=True)["index_key"] == built["index_key"]
        keys.append(built["index_key"])
        before = file_hash(index / "index_manifest.json")
        summary = run(
            adapter,
            dataset,
            ontology,
            "pilot",
            condition,
            index,
            tmp_path / "runs" / condition,
            ROOT / "configs/prompts/shared_generation.txt",
        )
        assert summary["cases"] == 6 and summary["valid_output_rate"] == 1
        assert summary["benchmark_eligible"] is False
        retrievals = read_jsonl(tmp_path / "runs" / condition / "retrieval.jsonl")
        assert all(r["native_status"] == "success" and r["retrieved_items"] for r in retrievals)
        assert all(
            any(i["mapping_status"] == "exact_quote" for i in r["retrieved_items"])
            for r in retrievals
        )
        for path in (tmp_path / "runs" / condition / "cases").glob("*/prompt.json"):
            envelope = json.loads(json.loads(path.read_text())["prompt"])["evidence"]
            for name, graph_rows in envelope["native_graph"].items():
                assert all(set(row) <= set(GRAPH_FIELDS[name]) for row in graph_rows)
            visible = json.dumps(envelope)
            for forbidden in ("created_at", "source_id", "gold_label", "mapped_assertion_ids"):
                assert forbidden not in visible
        assert (
            run(
                adapter,
                dataset,
                ontology,
                "pilot",
                condition,
                index,
                tmp_path / "runs" / condition,
                ROOT / "configs/prompts/shared_generation.txt",
                resume=True,
            )
            == summary
        )
        assert file_hash(index / "index_manifest.json") == before
        # Config changes must invalidate the snapshot, including prompts/models/settings.
        adapter.config["llm_model"] = "different-extractor"
        with pytest.raises(ValueError, match="cache identity changed"):
            adapter.index(corpus, index, resume=True)
        adapter.config["llm_model"] = "fixture-extractor-v1"
        sources = json.loads((index / "build/response.json").read_text())
        assert sources["status"] == "complete"
    assert len(set(keys)) == 2
