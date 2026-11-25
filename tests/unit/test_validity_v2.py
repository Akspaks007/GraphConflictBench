import copy
import json
from pathlib import Path

import pytest

from graphconflictbench.evidence_mapper import map_chunk
from graphconflictbench.generator import save_dataset
from graphconflictbench.inference import fixture_prediction
from graphconflictbench.manifests import canonical
from graphconflictbench.metrics import score_case
from graphconflictbench.prompts import GRAPH_FIELDS, build_prompt, evidence_envelope
from graphconflictbench.runner import normalize
from graphconflictbench.validator import Dataset

ROOT = Path(__file__).resolve().parents[2]


def evidence(tmp_path, ontology):
    save_dataset(tmp_path / "data", ontology, families=6)
    ds = Dataset(tmp_path / "data")
    case = next(c for c in ds.cases if c.hop_depth == 3 and c.gold_label)
    raw = {"status": "success", "data": {"chunks": [
        {"content": d.text, "file_path": d.doc_id + ".txt"} for d in ds.family(case)[2]
    ]}}
    return ds, case, raw, normalize(raw, ds, case, "test", 0.0, 4096, False)


@pytest.mark.parametrize("inject_after_normalization", [False, True])
def test_graph_metadata_allowlist_at_normalization_and_final_prompt(tmp_path, ontology,
                                                                  inject_after_normalization):
    ds, case, raw, retrieval = evidence(tmp_path, ontology)
    graph = {name: [{**{k: "source content" for k in fields},
                     "created_at": 123, "build_id": "SECRET_BUILD", "gold_label": True,
                     "hop_depth": 3, "mapped_assertion_ids": ["SECRET_EDGE"],
                     "nested": {"condition": "conflict"}, "source_id": "SECRET_CHUNK"}]
             for name, fields in GRAPH_FIELDS.items()}
    # A string path is not automatically safe, even when its field is allowlisted.
    graph["entities"][0]["file_path"] = "C:/private/conflict/gold.json"
    graph["entities"][0]["description"] = {"gold_label": True}
    original = copy.deepcopy(graph)
    if inject_after_normalization:
        retrieval.native_graph = graph
    else:
        raw["data"].update(graph)
        retrieval = normalize(raw, ds, case, "test", 0.0, 4096, False)
    _, prompt, _ = build_prompt(case, retrieval, ontology, ROOT / "configs/prompts/shared_generation.txt")
    for marker in ["created_at", "build_id", "gold_label", "hop_depth", "mapped_assertion_ids",
                   "SECRET_", "C:/private", '"condition"', '"source_id"']:
        assert marker not in prompt
    payload = json.loads(prompt)
    assert set(payload) == {"case_id", "question", "rules", "evidence", "response_schema"}
    assert graph == original  # Sanitization never rewrites the captured native object.
    for name, graph_rows in payload["evidence"]["native_graph"].items():
        assert all(set(row) <= set(GRAPH_FIELDS[name]) for row in graph_rows)


def test_opaque_source_allowlist_and_actual_budget(tmp_path, ontology):
    import tiktoken

    ds, case, raw, _ = evidence(tmp_path, ontology)
    d = ds.family(case)[2][0]
    raw["data"]["relationships"] = [{"src_id": case.subject, "tgt_id": case.target_object,
                                        "description": "Native summary", "created_at": 123,
                                        "file_path": d.doc_id + ".txt"}]
    original = copy.deepcopy(raw)
    retrieval = normalize(raw, ds, case, "test", 0.0, 4096, False)
    visible = canonical(evidence_envelope(retrieval))
    assert "created_at" not in visible
    assert raw == original
    assert retrieval.context_tokens == len(tiktoken.get_encoding("cl100k_base").encode(visible))
    assert retrieval.context_tokens <= 4096
    assert retrieval.native_graph["relationships"][0]["description"] == "Native summary"


def test_swapped_roles_fail_new_metric_but_preserve_legacy(tmp_path, ontology):
    ds, case, _, retrieval = evidence(tmp_path, ontology)
    prediction = fixture_prediction(case, retrieval)
    score = score_case(case, retrieval, prediction, ds.documents, ds.assertions)
    assert score["exact_proof_set"] and score["role_aware_exact_proof_set"]
    assert score["role_aware_localization_f1"] == 1
    c = prediction.conflicts[0]
    c.support, c.opposing = c.opposing, c.support
    swapped = score_case(case, retrieval, prediction, ds.documents, ds.assertions)
    assert swapped["exact_proof_set"] and swapped["localization_f1"] == 1
    assert not swapped["role_aware_exact_proof_set"]
    assert swapped["role_aware_localization_f1"] == 0
    assert swapped["support_localization_f1"] == swapped["opposing_localization_f1"] == 0


def test_role_metric_rejects_extra_nonassertion_and_split_witnesses(tmp_path, ontology):
    ds, case, _, retrieval = evidence(tmp_path, ontology)
    prediction = fixture_prediction(case, retrieval)
    extra = prediction.conflicts[0].support[0].model_copy(deep=True)
    extra.quote = "This registry entry"
    prediction.conflicts[0].support.append(extra)
    score = score_case(case, retrieval, prediction, ds.documents, ds.assertions)
    assert score["exact_proof_set"]  # Legacy compatibility includes this limitation.
    assert not score["role_aware_exact_proof_set"] and score["role_citation_errors"]
    prediction = fixture_prediction(case, retrieval)
    other = prediction.conflicts[0].model_copy(deep=True)
    prediction.conflicts[0].support = prediction.conflicts[0].support[:1]
    other.support = other.support[1:]
    prediction.conflicts.append(other)
    score = score_case(case, retrieval, prediction, ds.documents, ds.assertions)
    assert score["exact_proof_set"] and not score["role_aware_exact_proof_set"]


def test_role_citation_can_match_earlier_chunk_from_same_document(tmp_path, ontology):
    ds, case, _, retrieval = evidence(tmp_path, ontology)
    prediction = fixture_prediction(case, retrieval)
    doc_id = prediction.conflicts[0].support[0].doc_id
    d = next(d for d in ds.documents if d.doc_id == doc_id)
    later = map_chunk({"file_path": doc_id + ".txt", "content": "This registry entry"},
                      ds.documents, ds.assertions, len(retrieval.retrieved_items) + 1)
    retrieval.retrieved_items.append(later)
    assert later.text in d.text
    score = score_case(case, retrieval, prediction, ds.documents, ds.assertions)
    assert score["role_aware_exact_proof_set"]


def test_invalid_answer_does_not_hide_complete_retrieved_proof(tmp_path, ontology):
    ds, case, _, retrieval = evidence(tmp_path, ontology)
    score = score_case(case, retrieval, None, ds.documents, ds.assertions)
    assert score["outcome"] == "error"
    assert score["complete_proof_retrieved"] is True
    assert score["role_aware_exact_proof_set"] is False


def test_native_trace_refuses_overwrite(tmp_path):
    from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter

    (tmp_path / "response.json").write_text("original native response")
    adapter = LightRAGAdapter(ROOT / "configs/architectures/lightrag-fixture.yaml", "unused")
    with pytest.raises(ValueError, match="fresh attempt"):
        adapter._call("retrieve", tmp_path)
    assert (tmp_path / "response.json").read_text() == "original native response"


def test_failed_generation_preserves_attempt_prompt_and_retrieval(tmp_path, ontology, monkeypatch):
    from graphconflictbench import runner
    from graphconflictbench.manifests import file_hash, write_json

    ds, case, raw, _ = evidence(tmp_path, ontology)
    cm = json.loads((tmp_path / "data/corpora/pilot/conflict/corpus_manifest.json").read_text())
    index = tmp_path / "index"
    write_json(index / "index_manifest.json", {"architecture": "lightrag", "index_key": "offline",
        "identity": {"condition": "conflict", "split": "pilot", "corpus_hash": cm["corpus_hash"],
    }})

    class Adapter:
        config = {"architecture": "lightrag", "provider": "fixture", "benchmark_eligible": False}

        def retrieve(self, query, directory, budget, trace_dir):
            write_json(Path(trace_dir) / "response.json", {"raw": raw})
            return {"raw": raw}

    original_generate = runner.generate_prediction

    def fail(*args):
        raise RuntimeError("offline generation interruption")

    monkeypatch.setattr(runner, "generate_prediction", fail)
    output = tmp_path / "run"
    args = (Adapter(), tmp_path / "data", ontology, "pilot", "conflict", index, output,
            ROOT / "configs/prompts/shared_generation.txt")
    with pytest.raises(RuntimeError, match="interruption"):
        runner.run(*args, limit=1)
    first_case = ds.select("pilot", "conflict")[0]
    attempt = output / "cases" / first_case.case_id / "attempt-1"
    assert (attempt / "retrieval.json").is_file() and (attempt / "error.json").is_file()
    before = file_hash(attempt / "prompt.json")
    monkeypatch.setattr(runner, "generate_prediction", original_generate)
    runner.run(*args, limit=1, resume=True)
    assert file_hash(attempt / "prompt.json") == before
    assert (attempt.parent / "attempt-2/prompt.json").is_file()
