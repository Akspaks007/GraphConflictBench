"""Offline human-review preparation; never calls an inference provider.

Run with .venv-lightrag/Scripts/python.exe from the repository root.
Only writes new review artifacts next to this file. Original data is read-only.
"""

import csv
import html
import io
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, deque
from pathlib import Path

import tiktoken
import yaml
from lightrag.constants import DEFAULT_MAX_EXTRACTION_ENTITIES, DEFAULT_MAX_EXTRACTION_RECORDS
from lightrag.prompt import PROMPTS, resolve_entity_extraction_prompt_profile

from graphconflictbench.evidence_mapper import map_chunk
from graphconflictbench.manifests import canonical, file_hash, verify_checksums
from graphconflictbench.metrics import score_case
from graphconflictbench.models import parse_statements
from graphconflictbench.prompts import build_prompt
from graphconflictbench.reasoner import Ontology, Reasoner
from graphconflictbench.schemas import Prediction, Retrieval
from graphconflictbench.validator import Dataset, validate_dataset

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
PILOT = ROOT / "data/generated/pilot"
SAVED = ROOT / "results/lightrag-pilot"
ENC = tiktoken.get_encoding("cl100k_base")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    return [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]


def independent_shortest(assertions, subject, predicate, target):
    """Independent breadth-first positive path enumeration for this timeless pilot."""
    queue = deque([(subject, [], {subject})])
    found = []
    depth = None
    while queue:
        node, path, seen = queue.popleft()
        if depth is not None and len(path) >= depth:
            continue
        for a in assertions:
            if a.polarity != "positive" or a.subject != node or a.predicate != predicate:
                continue
            if a.object in seen:
                continue
            extended = path + [a.assertion_id]
            if a.object == target:
                found.append(extended)
                depth = len(extended)
            else:
                queue.append((a.object, extended, seen | {a.object}))
    return sorted(found)


def nested_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from nested_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_keys(item)


def count(text):
    return len(ENC.encode(text))


def main():
    ds = Dataset(PILOT)
    ontology = Ontology.load(ROOT / "configs/ontology.yaml")
    audit = validate_dataset(PILOT, ontology)
    assert all(a.valid_from is None and a.valid_to is None for a in ds.assertions)
    doc_by_id = {d.doc_id: d for d in ds.documents}
    edge_by_id = {a.assertion_id: a for a in ds.assertions}
    certificates = {(p["family_id"], p["condition"]): p for p in ds.proofs}
    corpus_ids = {}
    native_fidelity = {}
    problems = []
    graph_ns = {"g": "http://graphml.graphdrawing.org/xmlns"}
    for condition in ("conflict", "control"):
        index = SAVED / "indexes" / condition
        manifest = load(index / "index_manifest.json")
        verify_checksums(index, manifest["checksums"])
        expected_rows = rows(PILOT / "corpora/pilot" / condition / "documents.jsonl")
        assert rows(index / "corpus.jsonl") == expected_rows
        assert all(set(r) == {"doc_id", "text", "file_path"} for r in expected_rows)
        ids = {r["doc_id"] for r in expected_rows}
        corpus_ids[condition] = ids
        native = index / "native"
        full_docs = load(native / "kv_store_full_docs.json")
        chunks = load(native / "kv_store_text_chunks.json")
        assert set(full_docs) == ids
        for doc_id in ids:
            assert full_docs[doc_id]["content"] == doc_by_id[doc_id].text
        for chunk_id, chunk in chunks.items():
            assert chunk["full_doc_id"] in ids
            d = doc_by_id[chunk["full_doc_id"]]
            assert chunk["content"] == d.text
            assert chunk["file_path"] == d.doc_id + ".txt"
            assert map_chunk(chunk, ds.documents, ds.assertions, 1).mapped_assertion_ids
        graph = ET.parse(native / "graph_chunk_entity_relation.graphml").getroot()
        keys = {k.attrib["id"]: k.attrib["attr.name"] for k in graph.findall("g:key", graph_ns)}
        graph_edges = []
        for edge in graph.findall(".//g:edge", graph_ns):
            data = {keys[d.attrib["key"]]: d.text or "" for d in edge.findall("g:data", graph_ns)}
            data.update(source=edge.attrib["source"], target=edge.attrib["target"])
            graph_edges.append(data)
        preserved, losses = [], []
        for a in ds.assertions:
            if a.doc_id not in ids:
                continue
            d = doc_by_id[a.doc_id]
            span = next(s for s in d.sentence_spans if s.sentence_id == a.sentence_id)
            sentence = d.text[span.start:span.end]
            matches = [e for e in graph_edges if a.doc_id + ".txt" in e.get("file_path", "").split("<SEP>") and sentence in e.get("description", "") and {a.subject, a.object} == {e["source"], e["target"]}]
            (preserved if matches else losses).append(a.assertion_id)
        if losses:
            problems.append({"kind": "native_fixture_graph_quote_loss", "condition": condition, "assertions": losses})
        native_fidelity[condition] = {
            "documents": len(full_docs), "chunks": len(chunks),
            "exact_full_documents": len(ids), "exact_source_chunks": len(chunks),
            "graph_directed": graph.find("g:graph", graph_ns).attrib["edgedefault"],
            "graph_nodes": len(graph.findall(".//g:node", graph_ns)),
            "graph_edges": len(graph_edges),
            "assertions_found_verbatim_in_attributed_graph_descriptions": len(preserved),
            "assertions_not_found_verbatim_in_attributed_graph_descriptions": losses,
            "meaning": "Offline fixture snapshot inspection; not a live-model fidelity measurement or native directed proof alignment.",
        }

    shared = corpus_ids["conflict"] & corpus_ids["control"]
    assert shared == {d.doc_id for d in ds.documents if d.condition == "shared"}
    forbidden = {"gold_label", "gold_proof_sets", "gold_conflict_pairs", "mapped_assertion_ids", "mapping_status", "negative_edge_id", "minimal_support_edge_sets", "hop_depth", "family_id", "condition", "certificate_hash", "ontology_hash", "graph_hash"}
    inspection = {}
    evidence_counts = Counter()
    warnings = Counter()
    timestamp_values = {c: [] for c in ("conflict", "control")}
    graph_row_counts = {c: Counter() for c in ("conflict", "control")}
    for condition in ("conflict", "control"):
        run_dir = SAVED / "runs" / condition
        manifest = load(run_dir / "run_manifest.json")
        verify_checksums(run_dir, manifest["checksums"])
        for case in ds.select("pilot", condition):
            job = run_dir / "cases" / case.case_id
            retrieval = Retrieval.model_validate(load(job / "retrieval.json"))
            score = load(job / "score.json")
            stored_prompt = load(job / "prompt.json")
            system, prompt, prompt_hash = build_prompt(case, retrieval, ontology, ROOT / "configs/prompts/shared_generation.txt")
            assert stored_prompt == {"system": system, "prompt": prompt, "hash": prompt_hash}
            payload = json.loads(prompt)
            assert set(payload) == {"case_id", "question", "rules", "evidence", "response_schema"}
            assert not (set(nested_keys(payload)) & forbidden)
            assert not (set(re.findall(r"\bE[0-9a-f]{20}\b", prompt)) & set(edge_by_id))
            assert re.fullmatch(r"C[0-9a-f]{20}", case.case_id)
            prompt_docs = set(re.findall(r"\bD[0-9a-f]{20}\b", prompt))
            assert prompt_docs <= corpus_ids[condition]
            raw_response = load(job / "native-1/response.json")["raw"]
            raw_chunks = raw_response.get("data", {}).get("chunks", [])
            raw_maps = [map_chunk(c, ds.documents, ds.assertions, i + 1) for i, c in enumerate(raw_chunks)]
            for i in raw_maps:
                assert i.doc_id in corpus_ids[condition]
                assert i.text in doc_by_id[i.doc_id].text
            for item in retrieval.retrieved_items:
                assert item.doc_id in corpus_ids[condition]
                assert item.text in doc_by_id[item.doc_id].text
                original = next(i for i in raw_maps if i.native_chunk_id == item.native_chunk_id)
                assert item.mapped_assertion_ids == original.mapped_assertion_ids
                assert item.text == original.text
            delivered = {a for i in retrieval.retrieved_items for a in i.mapped_assertion_ids}
            before_budget = {a for i in raw_maps for a in i.mapped_assertion_ids}
            _, assertions, documents = ds.family(case)
            reasoner = Reasoner(ds.family(case)[0], assertions, ontology)
            denial = edge_by_id[case.negative_edge_id]
            positive_paths = independent_shortest(assertions, case.subject, case.relation_family, case.target_object)
            denial_paths = independent_shortest(assertions, denial.subject, denial.predicate, denial.object)
            assert positive_paths == [list(p) for p in reasoner.shortest_proofs(case.subject, case.relation_family, case.target_object)]
            assert bool(denial_paths) == case.gold_label
            assert all(len(p) == case.hop_depth for p in positive_paths)
            assert sorted(sorted(p + [denial.assertion_id]) for p in denial_paths) == sorted(sorted(p) for p in case.gold_proof_sets)
            assert certificates[(case.family_id, case.condition)] == reasoner.certificate(case)
            for a in assertions:
                assert parse_statements(doc_by_id[a.doc_id].text) == [(a.subject, a.predicate, a.polarity == "positive", a.object, doc_by_id[a.doc_id].text.split(". ", 1)[0] + ".")]
            partner = next(c for c in ds.cases if c.family_id == case.family_id and c.condition != condition)
            assert case.query == partner.query and case.hop_depth == partner.hop_depth
            assert case.relation_family == partner.relation_family and case.split == partner.split
            other_denial = edge_by_id[partner.negative_edge_id]
            assert (denial.subject, denial.predicate, denial.polarity, denial.valid_from, denial.valid_to) == (other_denial.subject, other_denial.predicate, other_denial.polarity, other_denial.valid_from, other_denial.valid_to)
            assert denial.object != other_denial.object
            missing = [[a for a in witness if a not in delivered] for witness in case.gold_proof_sets]
            missing_before = [[a for a in witness if a not in before_budget] for witness in case.gold_proof_sets]
            graph_text = canonical(raw_response.get("data", {}).get("relationships", []))
            graph_mentions_missing = [a for witness in missing for a in witness if doc_by_id[edge_by_id[a].doc_id].text.split(". ", 1)[0] + "." in graph_text]
            flags = ["human_signoff_pending", "synthetic_rule_scope_and_opaque_names"]
            timestamps = [int(row["created_at"]) for values in retrieval.native_graph.values() for row in values if row.get("created_at") is not None]
            timestamp_values[condition].extend(timestamps)
            graph_row_counts[condition].update({k: len(v) for k, v in retrieval.native_graph.items()})
            if timestamps:
                flags.append("model_visible_build_timestamp_condition_proxy")
            if not case.gold_label:
                flags.append("control_depth_labels_separate_positive_chain")
            if case.hop_depth == 1 and case.gold_label:
                flags.append("positive_and_denial_share_one_undirected_native_edge")
            if score["failure"]:
                flags.append("saved_fixture_" + score["failure"])
            warnings.update(retrieval.adapter_warnings)
            evidence_counts.update(raw_chunks=len(raw_maps), delivered_chunks=len(retrieval.retrieved_items), exact_raw_chunks=sum(bool(i.mapped_assertion_ids) for i in raw_maps), exact_delivered_chunks=sum(bool(i.mapped_assertion_ids) for i in retrieval.retrieved_items))
            inspection[case.case_id] = {
                "case": case.model_dump(mode="json"), "paired_case_id": partner.case_id,
                "documents": [d.model_dump(mode="json") for d in documents],
                "assertions": [a.model_dump(mode="json") for a in assertions],
                "positive_chain_shortest_paths": positive_paths,
                "paths_to_denied_object": denial_paths,
                "opposing_assertion": denial.model_dump(mode="json"),
                "stored_fixture_score": score,
                "missing_witness_assertions_after_budget": missing,
                "missing_witness_assertions_before_budget": missing_before,
                "missing_assertions_quoted_in_raw_graph_descriptions": sorted(set(graph_mentions_missing)),
                "model_prompt_input_tokens_cl100k_text_only": count(system) + count(prompt),
                "evidence_tokens": retrieval.context_tokens,
                "raw_chunk_count": len(raw_maps), "delivered_chunk_count": len(retrieval.retrieved_items),
                "warnings": retrieval.adapter_warnings, "review_flags": flags,
                "model_visible_created_at_range": [min(timestamps), max(timestamps)] if timestamps else None,
            }

    # Demonstrate a scorer limitation offline using a saved, schema-valid fixture response.
    good_case = next(c for c in ds.cases if c.gold_label and inspection[c.case_id]["stored_fixture_score"]["exact_proof_set"])
    good_job = SAVED / "runs/conflict/cases" / good_case.case_id
    good_pred = Prediction.model_validate(load(good_job / "prediction.json")["prediction"])
    swapped = good_pred.model_copy(deep=True)
    for conflict in swapped.conflicts:
        conflict.support, conflict.opposing = conflict.opposing, conflict.support
    swapped_score = score_case(good_case, Retrieval.model_validate(load(good_job / "retrieval.json")), swapped, ds.documents, ds.assertions)
    assert swapped_score["exact_proof_set"]
    scorer_probe = {"case_id": good_case.case_id, "operation": "Swap support and opposing citation lists in memory; no saved prediction was changed.", "exact_proof_set_after_swap": swapped_score["exact_proof_set"], "limitation": "The current scorer compares the union of cited assertions and does not validate citation roles."}

    smoke = Dataset(OUT / "smoke-dataset")
    smoke_audit = validate_dataset(OUT / "smoke-dataset", ontology)
    profile = resolve_entity_extraction_prompt_profile({}, False)
    context = {"tuple_delimiter": PROMPTS["DEFAULT_TUPLE_DELIMITER"], "completion_delimiter": PROMPTS["DEFAULT_COMPLETION_DELIMITER"], "entity_types_guidance": profile["entity_types_guidance"], "language": "English"}
    context.update(examples="\n".join(profile["entity_extraction_examples"]).format(**context), max_total_records=DEFAULT_MAX_EXTRACTION_RECORDS, max_entity_records=DEFAULT_MAX_EXTRACTION_ENTITIES)
    extraction_system = PROMPTS["entity_extraction_system_prompt"].format(**context)
    initial_inputs, glean_inputs, keyword_inputs = [], [], []
    for condition in ("conflict", "control"):
        for row in rows(OUT / "smoke-dataset/corpora/pilot" / condition / "documents.jsonl"):
            user = PROMPTS["entity_extraction_user_prompt"].format(**context, input_text=row["text"], heading_context_block="")
            glean = PROMPTS["entity_continue_extraction_user_prompt"].format(**context, input_text=row["text"])
            initial_inputs.append(count(extraction_system) + count(user) + 12)
            glean_inputs.append(count(extraction_system) + count(user) + 300 + count(glean) + 20)
        for case in smoke.select("pilot", condition):
            kw = PROMPTS["keywords_extraction"].format(query=case.query, examples="\n".join(PROMPTS["keywords_extraction_examples"]), language="English")
            keyword_inputs.append(count(kw) + 8)
    rates = {"llm_input_per_million_usd": 0.15, "llm_output_per_million_usd": 0.60, "embedding_per_million_usd": 0.02}
    stages = [
        {"stage": "initial extraction", "calls": 60, "input_tokens": sum(initial_inputs), "output_tokens": 60 * 300},
        {"stage": "one gleaning pass", "calls": 60, "input_tokens": sum(glean_inputs), "output_tokens": 60 * 100},
        {"stage": "entity/relation summaries allowance", "calls": 12, "input_tokens": 12 * 2000, "output_tokens": 12 * 400},
        {"stage": "retrieval keyword extraction", "calls": 12, "input_tokens": sum(keyword_inputs), "output_tokens": 12 * 150},
        {"stage": "final JSON generation", "calls": 12, "input_tokens": 12 * 5500, "output_tokens": 12 * 800},
    ]
    for stage in stages:
        stage["estimated_usd"] = (stage["input_tokens"] * 0.15 + stage["output_tokens"] * 0.60) / 1_000_000
    cost = {"kind": "offline_estimate_not_observed_usage", "rates": rates, "stages": stages, "embedding_tokens_allowance": 50000, "embedding_estimated_usd": 0.001, "central_total_usd": sum(s["estimated_usd"] for s in stages) + 0.001, "estimated_range_usd": [0.05, 0.30], "stress_envelope_usd": (2_000_000 * 0.15 + 250_000 * 0.60 + 200_000 * 0.02) / 1_000_000, "proposed_hard_cap_usd": 2.0, "application_can_enforce_hard_cap": False, "default_llm_completion_limit_sent": False, "source_document_tokens_across_both_smoke_conditions": sum(count(r["text"]) for c in ("conflict", "control") for r in rows(OUT / "smoke-dataset/corpora/pilot" / c / "documents.jsonl")), "initial_extraction_input_tokens_range": [min(initial_inputs), max(initial_inputs)], "note": "Text token counts use cl100k_base; actual model billing tokenizer, native descriptions, embeddings and summaries vary. Output tokens, 12 summaries, 5500 generation input tokens, and embedding allowance are assumptions; no cached-input or Batch discount. Calls are model callback invocations, not a guaranteed HTTP request bound."}

    manifest = load(ROOT / "ARTIFACT_MANIFEST.json")
    integrity = {"files_checked": len(manifest["sha256"]), "mismatches": [p for p, h in manifest["sha256"].items() if not (ROOT / p).is_file() or file_hash(ROOT / p) != h]}
    assert not integrity["mismatches"]
    metadata_leakage = {
        "kind": "observed_in_sample_condition_proxy_not_a_trained_leakage_classifier",
        "created_at_ranges": {c: {"min": min(v), "max": max(v), "rows": len(v)} for c, v in timestamp_values.items()},
        "ranges_nonoverlapping": max(timestamp_values["conflict"]) < min(timestamp_values["control"]),
        "cases_with_visible_timestamps": sum(bool(v["model_visible_created_at_range"]) for v in inspection.values()),
        "delivered_native_graph_row_counts": {c: dict(v) for c, v in graph_row_counts.items()},
        "recommendation_not_implemented": "Keep raw rows in traces; exclude volatile build timestamps from model-visible envelopes using a reviewed allowlist, then use fresh snapshots. No label, source or proof changes.",
    }
    summary = {"date_asia_kolkata": "2026-11-15", "pilot_audit": audit, "independent_paths_and_labels_checked": len(inspection), "paired_families_checked": len(ds.cases) // 2, "original_artifact_integrity": integrity, "native_fixture_fidelity": native_fidelity, "condition_isolation": {"shared_documents": len(shared), "conflict_only": len(corpus_ids["conflict"] - shared), "control_only": len(corpus_ids["control"] - shared)}, "saved_prompts_rebuilt_and_checked": len(inspection), "forbidden_gold_fields_in_saved_model_payloads": 0, "wrong_condition_document_ids_in_saved_model_payloads": 0, "evidence_chunk_counts": dict(evidence_counts), "retrieval_warning_case_counts": dict(warnings), "fixture_failure_case_ids": [k for k, v in inspection.items() if v["stored_fixture_score"]["failure"]], "review_flag_counts": dict(Counter(f for v in inspection.values() for f in v["review_flags"])), "scorer_role_probe": scorer_probe, "smoke": {"audit": smoke_audit, "relation_counts": dict(Counter(c.relation_family for c in smoke.cases)), "case_ids": [c.case_id for c in smoke.cases], "overlap_with_pilot_cases": len({c.case_id for c in smoke.cases} & set(inspection)), "documents_per_condition": {c: len(rows(OUT / "smoke-dataset/corpora/pilot" / c / "documents.jsonl")) for c in ("conflict", "control")}}, "cost_estimate": cost, "fidelity_problems": problems, "human_review_completed": False, "trained_leakage_classifier_run": False, "paid_model_calls": 0}

    summary["metadata_leakage"] = metadata_leakage
    # Human-only artifacts contain gold labels. They must never be native corpus inputs.
    markdown = ["# Pilot case review — human reviewers only", "", "48 cases / 24 paired families. Generated 15 November 2026. This artifact contains gold labels and canonical witnesses: never index it or add it to generation prompts. Automated logical verification is complete; human approval is pending. All original texts are reproduced verbatim. Readiness is blocked by the model-visible build timestamp condition proxy described in benchmark_readiness.md.", "", "Each case lists only its relevant family documents. Actual native retrieval searches the full 120-document condition corpus, including other families. Edge-role annotations and shortest paths below are reviewer-only.", "", "For controls, hop depth labels the separate positive chain to the canonical target. There is no positive proof to the explicitly denied alternative object. No conflict demonstrated is an open-world conclusion, not a declaration that the denial or any source is true.", "", "## Case index", "", "| Case | Pair family | Condition | Depth | Predicate | Saved fixture outcome | Attention |", "| --- | --- | --- | --- | --- | --- | --- |"]
    csv_buffer = io.StringIO(newline="")
    fieldnames = ["case_id", "paired_case_id", "family_id", "condition", "hop_depth", "relation_family", "expected_conflict", "automated_checks", "saved_fixture_failure", "review_flags", "reviewer", "review_date", "text_matches_assertions", "shortest_paths_valid", "denial_and_control_semantics_clear", "pair_and_isolation_valid", "no_unintended_label_cues", "native_polarity_and_direction_reviewed", "evidence_and_citations_faithful", "decision", "notes"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    sections = []
    html_sections = []
    for case in ds.cases:
        record = inspection[case.case_id]
        denial = edge_by_id[case.negative_edge_id]
        fail = record["stored_fixture_score"]["failure"]
        flags = record["review_flags"]
        markdown.append(f"| [{case.case_id}](#{case.case_id.lower()}) | {case.family_id} | {case.condition} | {case.hop_depth} | {case.relation_family} | {record['stored_fixture_score']['outcome']} | {'; '.join(flags)} |")
        section = [f"## {case.case_id}", "", f"Pair: **{case.family_id}** / partner **{record['paired_case_id']}**. Condition: **{case.condition}**. Expected conflict: **{str(case.gold_label).lower()}**. Minimum positive-chain depth: **{case.hop_depth}**. Relation: **{case.relation_family}**.", "", "### Question", "", case.query, "", "### Opposing / explicit negative assertion", "", f"`{denial.assertion_id}` from `{denial.doc_id}`: `{denial.subject} --NOT {denial.predicate}--> {denial.object}`.", "", f"Canonical positive-chain target: `{case.target_object}`. Denied object: `{denial.object}`.", "", "### All shortest positive source-backed paths", ""]
        proof_ids = {a for path in record["positive_chain_shortest_paths"] for a in path}
        for n, path in enumerate(record["positive_chain_shortest_paths"], 1):
            chain = case.subject + " " + " ".join(f"--{edge_by_id[a].predicate} [{a}; {edge_by_id[a].doc_id}]--> {edge_by_id[a].object}" for a in path)
            section.extend([f"Path {n} ({len(path)} supporting hops):", "", "```text", chain, "```", ""])
        section.extend(["Conflict witness sets (support plus separate denial): `" + canonical(case.gold_proof_sets) + "`.", ""])
        if not case.gold_label:
            section.extend(["**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.", ""])
        section.extend(["### Source documents (verbatim)", ""])
        for d in record["documents"]:
            a = next(a for a in record["assertions"] if a["doc_id"] == d["doc_id"])
            role = "explicit denial" if a["polarity"] == "negative" else "shortest-path support" if a["assertion_id"] in proof_ids else "unrelated distractor"
            section.extend([f"**{d['doc_id']}** — {role}; assertion `{a['assertion_id']}`; sentence `s1`; span [{d['sentence_spans'][0]['start']}, {d['sentence_spans'][0]['end']}); SHA256 of canonical JSON text `{d['checksum']}`.", "", "> " + d["text"], ""])
        section.extend(["### Saved fixture evidence and attention", "", f"Outcome: **{record['stored_fixture_score']['outcome']}**; failure: **{fail or 'none'}**. Raw source chunks: {record['raw_chunk_count']}; delivered: {record['delivered_chunk_count']}; evidence tokens: {record['evidence_tokens']}.", "", f"Missing witness assertions before budget: `{canonical(record['missing_witness_assertions_before_budget'])}`; after budget: `{canonical(record['missing_witness_assertions_after_budget'])}`.", "", f"Missing witness sentences present in raw native graph descriptions: `{canonical(record['missing_assertions_quoted_in_raw_graph_descriptions'])}`. These do not count as exact source-chunk proof retrieval.", "", "Review flags: " + "; ".join(flags) + ".", "", "- [ ] Question/source wording matches intended fictional rule scope.", "- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.", "- [ ] Pair differs only in denied object; alternative condition is excluded.", "- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.", "- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.", "- [ ] Record reviewer, date, decision and rationale in human_review.csv.", ""])
        sections.extend(section)
        text = "\n".join(section)
        html_sections.append(f'<details class="case" data-search="{html.escape(case.case_id + " " + case.family_id + " " + case.condition + " " + case.relation_family + " " + " ".join(flags), quote=True)}"><summary>{html.escape(case.case_id)} · {case.condition} · depth {case.hop_depth} · {case.relation_family}' + (" · RETRIEVAL MISS" if fail else "") + f'</summary><pre>{html.escape(text)}</pre></details>')
        writer.writerow({"case_id": case.case_id, "paired_case_id": record["paired_case_id"], "family_id": case.family_id, "condition": case.condition, "hop_depth": case.hop_depth, "relation_family": case.relation_family, "expected_conflict": str(case.gold_label).lower(), "automated_checks": "passed", "saved_fixture_failure": fail or "", "review_flags": ";".join(flags)})
    markdown.extend(["", *sections])
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GraphConflictBench pilot review</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#17243a;background:#f6f8fb}h1{font-size:1.7rem}aside{padding:1rem;background:#fff1c2;border-left:5px solid #986b00}input{padding:.7rem;width:90%;margin:1rem 0}details{background:white;margin:.7rem 0;border:1px solid #ccd4e0;border-radius:5px}summary{padding:1rem;cursor:pointer;font-weight:600}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.65 ui-monospace,monospace;padding:1rem}button{padding:.5rem;margin:.5rem}@media print{input,button{display:none}details{break-before:page}}</style><h1>GraphConflictBench — 48-case pilot review</h1><aside><b>Human reviewers only: contains gold labels and proofs.</b> Never index this report or feed it to an evaluation model. Human signoff is pending. Source text is verbatim. All outcomes shown are fixture plumbing observations, not research results.</aside><p>Filter by case/family ID, condition, predicate or review flag. Open cases to inspect questions, documents, denial, all shortest paths and missing evidence. Record decisions in the accompanying human_review.csv.</p><input id="filter" aria-label="Filter cases" placeholder="Filter e.g. PRECEDES or saved_fixture_retrieval_incomplete"><button onclick="document.querySelectorAll(\'details\').forEach(d=>d.open=true)">Expand all</button><button onclick="document.querySelectorAll(\'details\').forEach(d=>d.open=false)">Collapse all</button><p id="count">48 cases</p>' + "".join(html_sections) + '<script>document.getElementById("filter").addEventListener("input",e=>{let n=0;document.querySelectorAll(".case").forEach(d=>{d.hidden=!d.dataset.search.toLowerCase().includes(e.target.value.toLowerCase());if(!d.hidden)n++});document.getElementById("count").textContent=n+" cases"});</script></html>'
    config = yaml.safe_load((ROOT / "configs/architectures/lightrag.yaml").read_text())
    config.update(llm_model="gpt-4o-mini-2024-07-18", max_concurrency=1, max_retries=0, benchmark_eligible=False)
    for name, content in {
        "audit_findings.json": json.dumps(summary, indent=2) + "\n",
        "case_review.json": json.dumps(list(inspection.values()), indent=2) + "\n",
        "case_review.md": "\n".join(markdown) + "\n",
        "case_review.html": page,
        "human_review.csv": csv_buffer.getvalue(),
        "real-smoke.proposed.yaml": "# PROPOSAL ONLY. No paid execution authorized. Deprecated model: see readiness report.\n" + yaml.safe_dump(config, sort_keys=False),
    }.items():
        (OUT / name).write_text(content, encoding="utf-8", newline="")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
