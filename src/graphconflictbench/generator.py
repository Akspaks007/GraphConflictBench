"""Deterministic fictional worlds, paired at the family level."""

import csv
import io
import random
from pathlib import Path

from .manifests import (
    atomic_text,
    digest,
    exclusive_lock,
    tree_checksums,
    verify_checksums,
    write_json,
    write_jsonl,
)
from .reasoner import Reasoner
from .schemas import Assertion, Case, Document, Entity, Span

PHRASES = {
    "CONTAINED_IN": "is contained in",
    "SUBREGION_OF": "is a subregion of",
    "PRECEDES": "precedes",
}
NEGATIONS = {
    "CONTAINED_IN": "is not contained in",
    "SUBREGION_OF": "is not a subregion of",
    "PRECEDES": "does not precede",
}


def neutral_id(prefix, *parts):
    return prefix + digest(parts)[:20]


def build_dataset(ontology, families=24, seed=42, pilot=True):
    if families < 3 or families % 3:
        raise ValueError("families must be a positive multiple of three (one per depth)")
    rng = random.Random(seed)
    split_map = {}
    for h in (1, 2, 3):
        ids = [f"F{h}{j:04d}" for j in range(families // 3)]
        rng.shuffle(ids)
        design, dev = round(len(ids) * 0.2), round(len(ids) * 0.2)
        for i, family_id in enumerate(ids):
            split_map[family_id] = (
                "pilot"
                if pilot
                else "design"
                if i < design
                else "dev"
                if i < design + dev
                else "test"
            )
    entities, documents, assertions, cases, certificates = [], [], [], [], []
    for h in (1, 2, 3):
        for j in range(families // 3):
            family_id = f"F{h}{j:04d}"
            split = split_map[family_id]
            predicate = list(PHRASES)[j % 3]
            kind = ontology.relations[predicate].domain
            local_entities = [
                Entity(
                    entity_id=neutral_id("N", seed, family_id, k),
                    name=neutral_id("N", seed, family_id, k),
                    type=kind,
                    family_id=family_id,
                )
                for k in range(h + 6)
            ]
            entities.extend(local_entities)
            names = [e.name for e in local_entities]
            # Names contain no chain-position, role, or condition identifiers.
            chain, unrelated = names[: h + 1], names[h + 1]
            shared_edges = []
            denial_edges = {}
            for role, s, o, polarity, condition in (
                [(f"support-{i}", chain[i], chain[i + 1], "positive", "shared") for i in range(h)]
                + [
                    ("denial", chain[0], chain[-1], "negative", "conflict"),
                    ("denial", chain[0], unrelated, "negative", "control"),
                ]
                + [
                    (f"distractor-{i}", names[h + 2], names[h + 3 + i], "positive", "shared")
                    for i in range(2)
                ]
            ):
                phrase = PHRASES[predicate] if polarity == "positive" else NEGATIONS[predicate]
                sentence = f"{s} {phrase} {o}."
                text = sentence + (
                    " This registry entry describes the stated relationship in the "
                    "current fictional reference world. The entry records a source "
                    "assertion without evaluating other registry entries."
                )
                doc_id = neutral_id("D", seed, family_id, text)
                edge_id = neutral_id("E", doc_id)
                documents.append(
                    Document(
                        doc_id=doc_id,
                        family_id=family_id,
                        condition=condition,
                        split=split,
                        text=text,
                        checksum=digest(text),
                        sentence_spans=[Span(sentence_id="s1", start=0, end=len(sentence))],
                    )
                )
                a = Assertion(
                    assertion_id=edge_id,
                    doc_id=doc_id,
                    sentence_id="s1",
                    subject=s,
                    predicate=predicate,
                    object=o,
                    polarity=polarity,
                )
                assertions.append(a)
                if condition == "shared":
                    shared_edges.append(a)
                else:
                    denial_edges[condition] = a
            query = (
                "Based only on the available source documents, is there an inconsistency "
                f"in the stated relationship involving {chain[0]}? If yes, identify each "
                "incompatible claim and cite the exact source statements needed to establish "
                "it. If not, say no conflict. Do not assume a missing claim is false."
            )
            for condition in ("conflict", "control"):
                denial = denial_edges[condition]
                reasoner = Reasoner(local_entities, shared_edges + [denial], ontology)
                conflicts = reasoner.conflicts()
                witnesses = [
                    sorted([*proof, c["negative_edge_id"]])
                    for c in conflicts
                    for proof in c["minimal_support_edge_sets"]
                ]
                case = Case(
                    case_id=neutral_id("C", seed, family_id, condition),
                    family_id=family_id,
                    split=split,
                    condition=condition,
                    hop_depth=h,
                    relation_family=predicate,
                    query=query,
                    subject=chain[0],
                    target_object=chain[-1],
                    negative_edge_id=denial.assertion_id,
                    gold_label=condition == "conflict",
                    gold_proof_sets=witnesses,
                    gold_conflict_pairs=conflicts,
                )
                cases.append(case)
                certificates.append(reasoner.certificate(case))
    return {
        "entities": entities,
        "documents": documents,
        "assertions": assertions,
        "cases": cases,
        "proofs": certificates,
    }


def save_dataset(output, ontology, families=24, seed=42, pilot=True, resume=False):
    output = Path(output)
    identity = {
        "schema_version": "1.0",
        "generator_version": "1.0",
        "seed": seed,
        "families": families,
        "pilot": pilot,
        "ontology_hash": digest(ontology.model_dump(mode="json")),
    }
    with exclusive_lock(output):
        if (output / "dataset_manifest.json").exists():
            import json

            manifest = json.loads((output / "dataset_manifest.json").read_text())
            if resume and manifest["identity"] == identity:
                verify_checksums(output, manifest["checksums"])
                return manifest
            raise ValueError("dataset exists; choose a new directory or checksum-matching --resume")
        if any(p.name != ".job.lock" for p in output.iterdir()):
            raise ValueError("refusing to overwrite an incomplete/nonempty dataset directory")
        dataset = build_dataset(ontology, families, seed, pilot)
        for name, rows in dataset.items():
            write_jsonl(output / f"{name}.jsonl", rows)
        docs = dataset["documents"]
        for split in sorted({d.split for d in docs}):
            for condition in ("conflict", "control"):
                selected = sorted(
                    [d for d in docs if d.split == split and d.condition in ("shared", condition)],
                    key=lambda d: d.doc_id,
                )
                # Only these fields cross the native indexing boundary.
                corpus = [
                    {"doc_id": d.doc_id, "text": d.text, "file_path": d.doc_id + ".txt"}
                    for d in selected
                ]
                target = output / "corpora" / split / condition
                write_jsonl(target / "documents.jsonl", corpus)
                for d in selected:
                    atomic_text(target / "texts" / (d.doc_id + ".txt"), d.text)
                write_json(
                    target / "corpus_manifest.json",
                    {
                        "schema_version": "1.0",
                        "split": split,
                        "condition": condition,
                        "document_count": len(corpus),
                        "corpus_hash": digest(corpus),
                        "documents_file": "documents.jsonl",
                    },
                )
        sheet = io.StringIO()
        writer = csv.writer(sheet)
        writer.writerow(
            [
                "case_id",
                "relation_family",
                "hop_depth",
                "query",
                "reviewer",
                "text_matches_assertions",
                "no_shortcut",
                "label_valid",
                "notes",
            ]
        )
        for c in dataset["cases"]:
            writer.writerow(
                [c.case_id, c.relation_family, c.hop_depth, c.query, "", "", "", "", ""]
            )
        atomic_text(output / "human_audit.csv", sheet.getvalue())
        checksums = tree_checksums(output)
        manifest = {
            "identity": identity,
            "dataset_hash": digest({"identity": identity, "checksums": checksums}),
            "case_count": len(dataset["cases"]),
            "human_audited": False,
            "checksums": checksums,
        }
        write_json(output / "dataset_manifest.json", manifest)
        return manifest
