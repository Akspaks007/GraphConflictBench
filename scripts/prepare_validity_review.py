"""Replay captured evidence offline and prepare versioned Step 4 review materials.

No indexing, retrieval or provider calls. Does not regenerate the pilot or smoke
dataset. A replay is a presentation diagnostic, not a newly executed experiment.
"""

import argparse
import copy
import csv
import html
import io
import json
import statistics
from collections import Counter
from pathlib import Path

import tiktoken
import yaml

from graphconflictbench.manifests import canonical, file_hash, write_json
from graphconflictbench.prompts import (
    GRAPH_FIELDS,
    build_prompt,
    evidence_envelope,
    model_visible_graph,
)
from graphconflictbench.provider_control import ProviderPolicy
from graphconflictbench.reasoner import Ontology
from graphconflictbench.runner import normalize
from graphconflictbench.schemas import Retrieval
from graphconflictbench.validator import Dataset, validate_dataset


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--smoke-dataset", default="results/benchmark-readiness-20261115/smoke-dataset")
    args = parser.parse_args()
    root = Path.cwd()
    out = Path(args.output)
    if (out / "replay-report.json").exists():
        raise ValueError("review replay already exists; use a fresh versioned directory")
    out.mkdir(parents=True, exist_ok=True)
    ds = Dataset(root / "data/generated/pilot")
    ontology = Ontology.load(root / "configs/ontology.yaml")
    validate_dataset(ds.root, ontology)
    encoder = tiktoken.get_encoding("cl100k_base")
    def tokens(value):
        return len(encoder.encode(canonical(value)))
    replay_rows = []
    source_counts = Counter()
    budget = 4096
    for case in ds.cases:
        original_dir = root / "results/lightrag-pilot/runs" / case.condition / "cases" / case.case_id
        raw_path = original_dir / "native-1/response.json"
        raw_hash = file_hash(raw_path)
        raw = load(raw_path)["raw"]
        old = Retrieval.model_validate(load(original_dir / "retrieval.json"))
        new = normalize(raw, ds, case, "offline_presentation_replay_v2", 0.0, budget, False)
        system, prompt, prompt_hash = build_prompt(case, new, ontology,
                                                   root / "configs/prompts/shared_generation.txt")
        envelope = json.loads(prompt)["evidence"]
        for kind, rows in envelope["native_graph"].items():
            assert all(set(row) <= set(GRAPH_FIELDS[kind]) for row in rows)
        for forbidden in ("created_at", "source_id", "gold_label", "mapped_assertion_ids", "hop_depth"):
            assert forbidden not in prompt
        assert new.context_tokens <= budget
        assert [i.text for i in new.retrieved_items] == [i.text for i in old.retrieved_items]
        assert file_hash(raw_path) == raw_hash
        sources = evidence_envelope(new)["sources"]
        graph = model_visible_graph(raw.get("data", {}))
        diagnostic = {}
        for label, entity_rows, relation_rows in (
            ("historical_v1", old.native_graph["entities"], raw["data"]["relationships"]),
            ("allowlist_v2", new.native_graph["entities"], graph["relationships"]),
        ):
            prefix = {"sources": sources, "native_graph": {
                "entities": entity_rows, "relationships": [], "references": [],
            }}
            used = tokens(prefix)
            deltas = []
            for row in relation_rows:
                trial = copy.deepcopy(prefix)
                trial["native_graph"]["relationships"].append(row)
                deltas.append(tokens(trial) - used)
            diagnostic[label] = {
                "tokens_after_sources_and_retained_entities": used,
                "remaining_before_relationships": budget - used,
                "smallest_native_relationship_increment": min(deltas, default=None),
            }
        write_json(out / "prompt-replay-v2" / case.case_id / "prompt.json", {
            "kind": "offline_presentation_replay_not_provider_execution", "system": system,
            "prompt": prompt, "hash": prompt_hash, "original_raw_response_sha256": raw_hash,
        })
        write_json(out / "prompt-replay-v2" / case.case_id / "retrieval.json", new.model_dump())
        replay_rows.append({"case_id": case.case_id, "condition": case.condition,
                            "historical_graph_rows": {k: len(v) for k, v in old.native_graph.items()},
                            "v2_graph_rows": {k: len(v) for k, v in new.native_graph.items()},
                            "source_chunks": len(new.retrieved_items), "diagnostic": diagnostic})
        source_counts.update(chunks=len(new.retrieved_items))
    report = {
        "kind": "offline_presentation_replay_not_new_retrieval_or_generation",
        "cases": len(replay_rows), "evidence_budget": budget,
        "packing_order_unchanged": ["sources", "entities", "relationships", "references"],
        "source_chunk_occurrences_unchanged": source_counts["chunks"],
        "volatile_and_gold_field_leakage_cases_after_allowlist": 0,
        "historical_relationship_rows": sum(r["historical_graph_rows"]["relationships"] for r in replay_rows),
        "v2_relationship_rows": sum(r["v2_graph_rows"]["relationships"] for r in replay_rows),
        "v2_cases_with_relationship_rows": sum(bool(r["v2_graph_rows"]["relationships"]) for r in replay_rows),
        "median_remaining_tokens_before_relationships_v1": statistics.median(r["diagnostic"]["historical_v1"]["remaining_before_relationships"] for r in replay_rows),
        "median_remaining_tokens_before_relationships_v2": statistics.median(r["diagnostic"]["allowlist_v2"]["remaining_before_relationships"] for r in replay_rows),
        "cases_detail": replay_rows,
    }
    write_json(out / "replay-report.json", report)

    smoke_root = root / args.smoke_dataset
    smoke = Dataset(smoke_root)
    smoke_audit = validate_dataset(smoke_root, ontology)
    edges = {a.assertion_id: a for a in smoke.assertions}
    proofs = {(p["family_id"], p["condition"]): p for p in smoke.proofs}
    csv_stream = io.StringIO(newline="")
    fields = ["case_id", "paired_case_id", "family_id", "question", "expected_conflict",
              "condition", "hop_depth", "predicate", "source_documents_json",
              "opposing_assertion_json", "shortest_proof_paths_json", "conflict_witness_sets_json",
              "ambiguities", "reviewer", "date", "decision", "notes"]
    writer = csv.DictWriter(csv_stream, fieldnames=fields)
    writer.writeheader()
    sections = []
    md = ["# Twelve-case human-review worksheet (v2)", "",
          "Human-only gold material: never index this file or add it to model prompts. No human decision has been filled in. All twelve cases copy existing pilot texts, IDs, labels and proofs without alteration; this is not held-out evaluation. Source snapshot: " + str(smoke_root.relative_to(root)) + ". Predicates: " + ", ".join(sorted({c.relation_family for c in smoke.cases})) + ".", "",
          "Review each question, full source text, denial, supporting direction and shortest path. For controls, depth labels the separate positive chain, not a proof to the denied object. Record accept/question/reject and a reason in the accompanying CSV. All paths and role annotations below are canonical review aids, not native graph paths.", ""]
    for case in smoke.cases:
        _, assertions, docs = smoke.family(case)
        denial = edges[case.negative_edge_id]
        partner = next(c for c in smoke.cases if c.family_id == case.family_id and c.condition != case.condition)
        paths = proofs[(case.family_id, case.condition)]["minimal_support_edge_sets"]
        path_rows = [[{"assertion_id": a, "doc_id": edges[a].doc_id,
                       "subject": edges[a].subject, "predicate": edges[a].predicate,
                       "object": edges[a].object} for a in path] for path in paths]
        ambiguities = ["Human signoff pending; fictional ontology only; opaque names."]
        if not case.gold_label:
            ambiguities.append("Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims.")
        if case.gold_label and case.hop_depth == 1:
            ambiguities.append("Positive and negative claims merge on one undirected native endpoint pair; inspect both source sentences.")
        ambiguities.append("Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.")
        writer.writerow({"case_id": case.case_id, "paired_case_id": partner.case_id,
                         "family_id": case.family_id, "question": case.query,
                         "expected_conflict": str(case.gold_label).lower(), "condition": case.condition,
                         "hop_depth": case.hop_depth, "predicate": case.relation_family,
                         "source_documents_json": canonical([{"doc_id": d.doc_id, "text": d.text} for d in docs]),
                         "opposing_assertion_json": canonical(denial.model_dump(mode="json")),
                         "shortest_proof_paths_json": canonical(path_rows),
                         "conflict_witness_sets_json": canonical(case.gold_proof_sets),
                         "ambiguities": " ".join(ambiguities)})
        section = [f"## {case.case_id}", "", f"Pair {case.family_id}; partner {partner.case_id}. Condition **{case.condition}**, expected conflict **{case.gold_label}**, depth **{case.hop_depth}**, predicate **{case.relation_family}**.", "", "Question: " + case.query, "", "Opposing assertion: `" + canonical(denial.model_dump(mode="json")) + "`.", "", "All shortest positive proof paths:", ""]
        for path in path_rows:
            section.extend(["```text", "\n".join(f"{a['subject']} --{a['predicate']} [{a['assertion_id']}; {a['doc_id']}]--> {a['object']}" for a in path), "```", ""])
        section.extend(["Conflict witness sets (empty for controls): `" + canonical(case.gold_proof_sets) + "`.", "", "Source documents (verbatim):", ""])
        for d in docs:
            section.extend([f"**{d.doc_id}**", "", "> " + d.text, ""])
        section.extend(["Possible ambiguities / review attention: " + " ".join(ambiguities), "",
                        "- [ ] Source text, polarity and source spans are faithful.",
                        "- [ ] Shortest proof and denial roles are correct; control semantics are clear.",
                        "- [ ] Pair/isolation and live extraction fidelity reviewed.",
                        "- [ ] Reviewer, date, decision and rationale entered in CSV.", ""])
        md.extend(section)
        sections.append('<details><summary>' + html.escape(case.case_id + " / " + case.condition + " / depth " + str(case.hop_depth)) + '</summary><pre>' + html.escape("\n".join(section)) + '</pre></details>')
    (out / "human_review_smoke12.csv").write_text(csv_stream.getvalue(), encoding="utf-8", newline="")
    (out / "human_review_smoke12.md").write_text("\n".join(md), encoding="utf-8")
    (out / "human_review_smoke12.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Step 4 v2 smoke review</title><style>body{max-width:1100px;margin:2em auto;padding:1em;font:16px system-ui}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 monospace}details{border:1px solid #ccc;padding:1em;margin:1em 0}</style><h1>12-case human review — gold material</h1><p>Never index this document or supply it to the evaluation model. Human signoff is pending. All text and labels come from the unchanged smoke snapshot. Record decisions in the accompanying CSV.</p>' + "".join(sections) + '</html>', encoding="utf-8")
    write_json(out / "smoke-input-audit.json", smoke_audit)
    policy_file = out / "provider-policy.v2.json"
    policy = ProviderPolicy(llm_model="gpt-4o-mini-2024-07-18", embedding_model="text-embedding-3-small",
                            cap_nanodollars=2_000_000_000, llm_input_nanodollars_per_token=150,
                            llm_output_nanodollars_per_token=600, embedding_nanodollars_per_token=20,
                            max_completion_tokens=1536, max_request_input_tokens=128000,
                            state_directory="live-provider-control-v2")
    write_json(policy_file, policy.model_dump())
    config = yaml.safe_load((root / "results/benchmark-readiness-20261115/real-smoke.proposed.yaml").read_text())
    config.update(provider_control_file=str(policy_file.as_posix()),
                  provider_control_sha256=file_hash(policy_file))
    (out / "real-smoke.v2.yaml").write_text(
        "# Prepared only. Paid execution requires separate approval and human signoff.\n" + yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    print(canonical({k: v for k, v in report.items() if k != "cases_detail"}))


if __name__ == "__main__":
    main()
