"""Copy a declared balanced six-family pilot subset into a NEW smoke snapshot.

No assertion text, labels, IDs, proof depths or certificates are recomputed.
Selection is fixed by depth/predicate cells, not observed retrieval performance.
"""

import argparse
import json
from pathlib import Path

from graphconflictbench.manifests import (
    atomic_text,
    digest,
    tree_checksums,
    write_json,
    write_jsonl,
)
from graphconflictbench.reasoner import Ontology
from graphconflictbench.validator import Dataset, validate_dataset

FAMILIES = ("F10000", "F10001", "F20000", "F20002", "F30001", "F30002")


def prepare(source, target, ontology):
    validate_dataset(source, ontology)
    target = Path(target)
    target.mkdir(parents=True, exist_ok=False)
    ds = Dataset(source)
    entities = [x for x in ds.entities if x.family_id in FAMILIES]
    documents = [x for x in ds.documents if x.family_id in FAMILIES]
    doc_ids = {x.doc_id for x in documents}
    assertions = [x for x in ds.assertions if x.doc_id in doc_ids]
    cases = [x for x in ds.cases if x.family_id in FAMILIES]
    proofs = [x for x in ds.proofs if x["family_id"] in FAMILIES]
    assert len(cases) == 12 and len({c.family_id for c in cases}) == 6
    for name, records in (("entities", entities), ("documents", documents),
                          ("assertions", assertions), ("cases", cases), ("proofs", proofs)):
        write_jsonl(target / (name + ".jsonl"), records)
    for condition in ("conflict", "control"):
        selected = sorted([d for d in documents if d.condition in ("shared", condition)],
                          key=lambda d: d.doc_id)
        export = [{"doc_id": d.doc_id, "text": d.text, "file_path": d.doc_id + ".txt"}
                  for d in selected]
        directory = target / "corpora/pilot" / condition
        write_jsonl(directory / "documents.jsonl", export)
        for d in selected:
            atomic_text(directory / "texts" / (d.doc_id + ".txt"), d.text)
        write_json(directory / "corpus_manifest.json", {
            "schema_version": "1.0", "split": "pilot", "condition": condition,
            "document_count": len(export), "corpus_hash": digest(export),
            "documents_file": "documents.jsonl",
        })
    parent = json.loads((Path(source) / "dataset_manifest.json").read_text())
    identity = {"schema_version": "1.0", "selection_version": "stratified-smoke-v2",
                "parent_dataset_hash": parent["dataset_hash"], "families": list(FAMILIES),
                "selection_rule": "two families per depth and two per predicate; first eligible IDs in declared cells; not outcome-selected"}
    checksums = tree_checksums(target)
    write_json(target / "dataset_manifest.json", {
        "identity": identity, "dataset_hash": digest({"identity": identity, "checksums": checksums}),
        "case_count": len(cases), "human_audited": False, "checksums": checksums,
    })
    return validate_dataset(target, ontology)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="data/generated/pilot")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output, Ontology.load("configs/ontology.yaml")), indent=2))
