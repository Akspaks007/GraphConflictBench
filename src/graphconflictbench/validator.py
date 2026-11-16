"""Independent structural, provenance, pairing and logical dataset checks."""

import json
from collections import Counter, defaultdict
from pathlib import Path

from .generator import NEGATIONS, PHRASES
from .manifests import digest, read_jsonl, verify_checksums
from .reasoner import Reasoner
from .schemas import Assertion, Case, Document, Entity


def unique(rows, field):
    values = [getattr(x, field) for x in rows]
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {field}")


class Dataset:
    def __init__(self, root):
        self.root = Path(root)
        self.entities = read_jsonl(self.root / "entities.jsonl", Entity)
        self.documents = read_jsonl(self.root / "documents.jsonl", Document)
        self.assertions = read_jsonl(self.root / "assertions.jsonl", Assertion)
        self.cases = read_jsonl(self.root / "cases.jsonl", Case)
        self.proofs = read_jsonl(self.root / "proofs.jsonl")

    def family(self, case):
        docs = [
            d
            for d in self.documents
            if d.family_id == case.family_id and d.condition in ("shared", case.condition)
        ]
        ids = {d.doc_id for d in docs}
        return (
            [e for e in self.entities if e.family_id == case.family_id],
            [a for a in self.assertions if a.doc_id in ids],
            docs,
        )

    def select(self, split, condition=None):
        return [
            c
            for c in self.cases
            if c.split == split and (condition is None or c.condition == condition)
        ]


def validate_dataset(root, ontology, checksums=True):
    dataset = Dataset(root)
    manifest = json.loads((Path(root) / "dataset_manifest.json").read_text())
    if checksums:
        verify_checksums(root, manifest["checksums"])
    for rows, field in [
        (dataset.entities, "entity_id"),
        (dataset.documents, "doc_id"),
        (dataset.assertions, "assertion_id"),
        (dataset.cases, "case_id"),
    ]:
        unique(rows, field)
    if len({e.name for e in dataset.entities}) != len(dataset.entities):
        raise ValueError("duplicate entity name")
    docs = {d.doc_id: d for d in dataset.documents}
    entity_map = {e.entity_id: e for e in dataset.entities}
    for d in dataset.documents:
        if d.checksum != digest(d.text):
            raise ValueError("source text checksum mismatch")
        unique(d.sentence_spans, "sentence_id")
        if any(s.end > len(d.text) for s in d.sentence_spans):
            raise ValueError("sentence span outside source document")
    for a in dataset.assertions:
        if a.doc_id not in docs:
            raise ValueError("missing document provenance")
        d = docs[a.doc_id]
        spans = [s for s in d.sentence_spans if s.sentence_id == a.sentence_id]
        if len(spans) != 1:
            raise ValueError("missing sentence provenance")
        if a.subject not in entity_map or a.object not in entity_map:
            raise ValueError("unknown entity")
        if any(entity_map[x].family_id != d.family_id for x in (a.subject, a.object)):
            raise ValueError("entity/document family mismatch")
        phrase = (PHRASES if a.polarity == "positive" else NEGATIONS).get(a.predicate)
        if phrase is None:
            raise ValueError("unknown textual predicate")
        s = spans[0]
        if d.text[s.start : s.end] != f"{a.subject} {phrase} {a.object}.":
            raise ValueError("source statement does not express its canonical assertion")
    family_cases = defaultdict(list)
    certificates = {(p["family_id"], p["condition"]): p for p in dataset.proofs}
    if len(certificates) != len(dataset.cases):
        raise ValueError("duplicate/missing verification certificate")
    for c in dataset.cases:
        entities, assertions, source_docs = dataset.family(c)
        if not source_docs or any(d.split != c.split for d in source_docs):
            raise ValueError("case/document split mismatch")
        result = Reasoner(entities, assertions, ontology).certificate(c)
        if result != certificates[(c.family_id, c.condition)]:
            raise ValueError("certificate mismatch")
        family_cases[c.family_id].append(c)
    for family, variants in family_cases.items():
        if len(variants) != 2 or {c.condition for c in variants} != {"conflict", "control"}:
            raise ValueError("family must have exactly two paired conditions")
        if len({c.split for c in variants}) != 1 or len({c.query for c in variants}) != 1:
            raise ValueError("family split leakage or unpaired query")
        variant_docs = [
            d for d in dataset.documents if d.family_id == family and d.condition != "shared"
        ]
        if len(variant_docs) != 2:
            raise ValueError("paired conditions must differ in exactly one source assertion")
        a = {
            c.condition: next(a for a in dataset.assertions if a.assertion_id == c.negative_edge_id)
            for c in variants
        }
        if (a["conflict"].subject, a["conflict"].predicate, a["conflict"].polarity) != (
            a["control"].subject,
            a["control"].predicate,
            a["control"].polarity,
        ):
            raise ValueError("paired intervention changed more than the denied object")
    for path in sorted((dataset.root / "corpora").glob("*/*/corpus_manifest.json")):
        cm = json.loads(path.read_text())
        rows = read_jsonl(path.parent / cm["documents_file"])
        expected = [
            {"doc_id": d.doc_id, "text": d.text, "file_path": d.doc_id + ".txt"}
            for d in sorted(dataset.documents, key=lambda d: d.doc_id)
            if d.split == cm["split"] and d.condition in ("shared", cm["condition"])
        ]
        if rows != expected or cm["corpus_hash"] != digest(rows):
            raise ValueError("corpus contains cross-condition contamination or changed documents")
    # These are observed overlap checks, not a trained leakage classifier.
    return {
        "status": "passed",
        "cases": len(dataset.cases),
        "families": len(family_cases),
        "by_depth_condition": dict(
            sorted(Counter(f"{c.hop_depth}:{c.condition}" for c in dataset.cases).items())
        ),
        "documents": len(dataset.documents),
        "all_certificates_valid": True,
        "paired_queries_identical": True,
        "human_audit": "pending",
        "label_leakage_classifier": "not_run",
    }
