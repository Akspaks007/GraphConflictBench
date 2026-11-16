from pathlib import Path

import pytest

from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter
from graphconflictbench.evidence_mapper import map_chunk
from graphconflictbench.generator import save_dataset
from graphconflictbench.inference import fixture_prediction
from graphconflictbench.manifests import canonical, digest, write_json, write_jsonl
from graphconflictbench.metrics import aggregate, score_case
from graphconflictbench.prompts import evidence_envelope
from graphconflictbench.runner import normalize
from graphconflictbench.schemas import Retrieval
from graphconflictbench.validator import Dataset

ROOT = Path(__file__).resolve().parents[2]


def fixture_evidence(tmp_path, ontology):
    save_dataset(tmp_path / "data", ontology, families=6)
    ds = Dataset(tmp_path / "data")
    case = next(c for c in ds.cases if c.hop_depth == 3 and c.gold_label)
    _, assertions, docs = ds.family(case)
    items = [
        map_chunk({"content": d.text, "file_path": d.doc_id + ".txt"}, docs, assertions, i + 1)
        for i, d in enumerate(docs)
    ]
    r = Retrieval(
        run_id="TEST",
        case_id=case.case_id,
        retrieval_ms=0.0,
        context_tokens=100,
        retrieved_items=items,
        capture_complete=True,
        native_status="success",
        adapter_warnings=[],
        benchmark_eligible=False,
    )
    return ds, case, r


def test_exact_localization_and_retrieval_failure_are_separate(tmp_path, ontology):
    ds, case, r = fixture_evidence(tmp_path, ontology)
    prediction = fixture_prediction(case, r)
    perfect = score_case(case, r, prediction, ds.documents, ds.assertions)
    assert perfect["outcome"] == "tp" and perfect["exact_proof_set"]
    # Correctly guessing a conflict cannot hide a missing retrieved proof edge.
    missing = case.gold_proof_sets[0][0]
    r.retrieved_items = [i for i in r.retrieved_items if missing not in i.mapped_assertion_ids]
    guessed = score_case(case, r, prediction, ds.documents, ds.assertions)
    assert guessed["outcome"] == "tp"
    assert not guessed["complete_proof_retrieved"]
    assert guessed["failure"] == "retrieval_incomplete"


def test_wrong_quote_is_detection_success_localization_failure(tmp_path, ontology):
    ds, case, r = fixture_evidence(tmp_path, ontology)
    prediction = fixture_prediction(case, r)
    prediction.conflicts[0].support[0].quote = "An invented quote."
    score = score_case(case, r, prediction, ds.documents, ds.assertions)
    assert score["outcome"] == "tp" and score["failure"] == "localization_miss"
    assert not score["exact_proof_set"] and score["citation_errors"]


def test_source_id_alone_never_manufactures_edges(tmp_path, ontology):
    ds, _, r = fixture_evidence(tmp_path, ontology)
    d = ds.documents[0]
    item = map_chunk(
        {"content": "Summary without the original assertion.", "file_path": d.doc_id + ".txt"},
        ds.documents,
        ds.assertions,
        1,
    )
    assert not item.mapped_assertion_ids and item.mapping_status == "unmapped"
    assert "mapped_assertion_ids" not in canonical(evidence_envelope(r))


def test_envelope_budget_and_order(tmp_path, ontology):
    import tiktoken

    ds, case, _ = fixture_evidence(tmp_path, ontology)
    docs = ds.family(case)[2]
    raw = {
        "status": "success",
        "data": {"chunks": [{"content": d.text, "file_path": d.doc_id + ".txt"} for d in docs]},
    }
    r = normalize(raw, ds, case, "test", 0.0, 300, False)
    assert r.context_tokens <= 300
    assert r.context_tokens == len(
        tiktoken.get_encoding("cl100k_base").encode(canonical(evidence_envelope(r)))
    )
    assert [x.rank for x in r.retrieved_items] == list(range(1, len(r.retrieved_items) + 1))
    assert r.adapter_warnings


def test_confusion_totals_and_explicit_errors():
    rows = [{"outcome": k} for k in ["tp", "tp", "fn", "tn", "fp", "error"]]
    s = aggregate(rows)
    assert sum(s[k] for k in ("tp", "tn", "fp", "fn", "error")) == s["cases"] == 6
    assert s["f1_valid_rows"] == pytest.approx(2 / 3)
    assert s["valid_output_rate"] == pytest.approx(5 / 6)


def test_worker_interpreter_preserves_venv_symlink(tmp_path):
    interpreter = tmp_path / "python"
    interpreter.symlink_to("/usr/bin/python3")
    adapter = LightRAGAdapter(ROOT / "configs/architectures/lightrag-fixture.yaml", interpreter)
    assert adapter.worker_python == str(interpreter)


def test_index_rejects_mixed_boundary_fields_and_bad_hash(tmp_path):
    adapter = LightRAGAdapter(ROOT / "configs/architectures/lightrag-fixture.yaml", "unused")
    rows = [{"doc_id": "D", "text": "X", "file_path": "D.txt", "gold_label": True}]
    write_jsonl(tmp_path / "documents.jsonl", rows)
    write_json(
        tmp_path / "corpus_manifest.json",
        {
            "condition": "conflict",
            "split": "pilot",
            "document_count": 1,
            "corpus_hash": digest(rows),
            "documents_file": "documents.jsonl",
        },
    )
    with pytest.raises(ValueError, match="only raw documents"):
        adapter.index(tmp_path / "corpus_manifest.json", tmp_path / "index")


def test_modified_source_invalidates_dataset_resume(tmp_path, ontology):
    save_dataset(tmp_path, ontology, families=6)
    with (tmp_path / "documents.jsonl").open("a") as f:
        f.write("{}\n")
    with pytest.raises(ValueError, match="checksum"):
        save_dataset(tmp_path, ontology, families=6, resume=True)
