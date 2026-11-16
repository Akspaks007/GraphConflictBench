import json
from collections import defaultdict

import pytest

from graphconflictbench.generator import build_dataset, save_dataset
from graphconflictbench.manifests import digest, exclusive_lock, write_jsonl
from graphconflictbench.schemas import Document, Prediction
from graphconflictbench.validator import validate_dataset


def test_deterministic_paired_pilot_and_isolation(tmp_path, ontology):
    root = tmp_path / "pilot"
    save_dataset(root, ontology)
    report = validate_dataset(root, ontology)
    assert report["cases"] == 48
    assert all(n == 8 for n in report["by_depth_condition"].values())
    first = build_dataset(ontology)
    second = build_dataset(ontology)

    def as_json(ds):
        return {
            k: [x.model_dump(mode="json") if hasattr(x, "model_dump") else x for x in rows]
            for k, rows in ds.items()
        }

    assert digest(as_json(first)) == digest(as_json(second))
    assert save_dataset(root, ontology, resume=True)["case_count"] == 48
    with pytest.raises(ValueError):
        save_dataset(root, ontology, seed=7, resume=True)
    for c in first["cases"]:
        assert "conflict" not in c.case_id and "control" not in c.case_id


def test_full_matches_pdf_case_count_and_family_splits(ontology):
    ds = build_dataset(ontology, families=120, pilot=False)
    assert len(ds["cases"]) == 240
    by_family = defaultdict(set)
    for c in ds["cases"]:
        by_family[c.family_id].add(c.split)
    assert all(len(s) == 1 for s in by_family.values())
    assert {next(iter(s)) for s in by_family.values()} == {"design", "dev", "test"}


@pytest.mark.parametrize(
    "kind",
    [
        "duplicate_doc",
        "missing_provenance",
        "duplicate_sentence",
        "wrong_text",
        "shortcut",
        "mixed_conditions",
        "split_leak",
    ],
)
def test_audit_rejects_corruptions(tmp_path, ontology, kind):
    root = tmp_path / "data"
    save_dataset(root, ontology, families=6)

    def load(name):
        return [json.loads(x) for x in (root / f"{name}.jsonl").read_text().splitlines()]

    if kind in ("duplicate_doc", "duplicate_sentence", "wrong_text"):
        docs = load("documents")
        if kind == "duplicate_doc":
            docs.append(docs[0])
        elif kind == "duplicate_sentence":
            docs[0]["sentence_spans"].append(docs[0]["sentence_spans"][0])
        else:
            docs[0]["text"] = "Wrong source text."
        write_jsonl(root / "documents.jsonl", docs)
    elif kind == "missing_provenance":
        assertions = load("assertions")
        assertions[0]["doc_id"] = "MISSING"
        write_jsonl(root / "assertions.jsonl", assertions)
    elif kind in ("shortcut", "split_leak"):
        cases = load("cases")
        case = next(c for c in cases if c["hop_depth"] == 3)
        case["hop_depth" if kind == "shortcut" else "split"] = 2 if kind == "shortcut" else "dev"
        write_jsonl(root / "cases.jsonl", cases)
    else:
        path = root / "corpora/pilot/conflict/documents.jsonl"
        control = load("documents")
        row = next(d for d in control if d["condition"] == "control")
        with path.open("a") as f:
            f.write(
                json.dumps(
                    {
                        "doc_id": row["doc_id"],
                        "text": row["text"],
                        "file_path": row["doc_id"] + ".txt",
                    }
                )
                + "\n"
            )
    with pytest.raises(ValueError):
        validate_dataset(root, ontology, checksums=False)


def test_lock_prevents_concurrent_overwrite(tmp_path):
    with exclusive_lock(tmp_path):
        with pytest.raises(RuntimeError):
            with exclusive_lock(tmp_path):
                pass


def test_strict_schema_rejects_malformed_json_and_boolean_coercion():
    with pytest.raises(ValueError):
        Prediction.model_validate_json('{"case_id":')
    with pytest.raises(ValueError):
        Prediction(case_id="C", conflict_detected="false", evidence_status="complete", conflicts=[])
    with pytest.raises(ValueError):
        Document.model_validate({"doc_id": "D"})
