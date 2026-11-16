"""Offline verification of v2 artifacts; never initializes or calls a live provider."""

import argparse
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter, implementation_hash
from graphconflictbench.manifests import file_hash, verify_checksums, write_json
from graphconflictbench.prompts import GRAPH_FIELDS
from graphconflictbench.provider_control import ProviderControl
from graphconflictbench.reasoner import Ontology
from graphconflictbench.validator import Dataset, validate_dataset


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from keys(item)


def tests(path):
    suite = ET.parse(path).getroot().find("testsuite").attrib
    result = {k: int(suite[k]) for k in ("tests", "failures", "errors", "skipped")}
    assert result["failures"] == result["errors"] == result["skipped"] == 0
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path.cwd()
    out = root / args.output
    plan = out / "final-plan"
    original = load(root / "ARTIFACT_MANIFEST.json")
    with zipfile.ZipFile(out / "historical-step4.zip") as archive:
        assert archive.read("ARTIFACT_MANIFEST.json") == (root / "ARTIFACT_MANIFEST.json").read_bytes()
        assert all(hashlib.sha256(archive.read(p)).hexdigest() == h for p, h in original["sha256"].items())
    changed = [p for p, h in original["sha256"].items() if file_hash(root / p) != h]
    assert all(p == "README.md" or p.startswith("src/") or p.startswith("tests/") for p in changed)
    assert not any(p.startswith(("data/", "results/", "configs/", "docs/")) for p in changed)
    previous = root / "results/benchmark-readiness-20261115"
    verify_checksums(previous, load(previous / "REVIEW_MANIFEST.json")["sha256"])
    ontology = Ontology.load(root / "configs/ontology.yaml")
    pilot = Dataset(root / "data/generated/pilot")
    smoke = Dataset(out / "stratified-smoke-v2")
    for name, id_field in (("entities", "entity_id"), ("documents", "doc_id"),
                           ("assertions", "assertion_id"), ("cases", "case_id")):
        parent = {getattr(x, id_field): x.model_dump(mode="json") for x in getattr(pilot, name)}
        assert all(x.model_dump(mode="json") == parent[getattr(x, id_field)]
                   for x in getattr(smoke, name))
    assert all(p in pilot.proofs for p in smoke.proofs)
    assert Counter(c.relation_family for c in smoke.cases) == {
        "CONTAINED_IN": 4, "SUBREGION_OF": 4, "PRECEDES": 4,
    }
    worksheet = list(csv.DictReader((plan / "human_review_smoke12.csv").open(encoding="utf-8", newline="")))
    assert len(worksheet) == 12
    by_id = {c.case_id: c for c in smoke.cases}
    for row in worksheet:
        case = by_id[row["case_id"]]
        assert row["question"] == case.query and row["expected_conflict"] == str(case.gold_label).lower()
        assert not row["reviewer"] and not row["decision"]
        expected_docs = [{"doc_id": d.doc_id, "text": d.text} for d in smoke.family(case)[2]]
        assert json.loads(row["source_documents_json"]) == expected_docs
        assert json.loads(row["shortest_proof_paths_json"])
    prompt_paths = list((plan / "prompt-replay-v2").glob("*/prompt.json"))
    assert len(prompt_paths) == 48
    native = out / "stratified-fixture-v2"
    native_prompts = list((native / "runs").glob("*/cases/*/prompt.json"))
    assert len(native_prompts) == 12
    forbidden = {"created_at", "source_id", "gold_label", "gold_proof_sets", "gold_conflict_pairs",
                 "mapped_assertion_ids", "mapping_status", "condition", "family_id", "hop_depth",
                 "run_id", "build_id", "negative_edge_id", "minimal_support_edge_sets"}
    for path in prompt_paths + native_prompts:
        payload = json.loads(load(path)["prompt"])
        assert not (set(keys(payload)) & forbidden)
        assert not re.search(r"\bE[0-9a-f]{20}\b", load(path)["prompt"])
        for name, graph_rows in payload["evidence"]["native_graph"].items():
            assert all(set(row) <= set(GRAPH_FIELDS[name]) for row in graph_rows)
    fixture = {}
    for condition in ("conflict", "control"):
        index = native / "indexes" / condition
        manifest = load(index / "index_manifest.json")
        assert manifest["identity"]["implementation_hash"] == implementation_hash()
        assert manifest["build_result"]["documents_processed"] == 30
        verify_checksums(index, manifest["checksums"])
        run_dir = native / "runs" / condition
        verify_checksums(run_dir, load(run_dir / "run_manifest.json")["checksums"])
        summary = load(run_dir / "summary.json")
        assert summary["benchmark_eligible"] is False and summary["cases"] == 6
        assert summary["valid_output_rate"] == 1
        fixture[condition] = summary
    adapter = LightRAGAdapter(plan / "real-smoke.v2.yaml", root / ".venv-lightrag/Scripts/python.exe")
    policy = ProviderControl(adapter.config["provider_control_file"], adapter.config["provider_control_sha256"])
    assert not policy.root.exists()
    health = adapter.healthcheck()  # Distribution metadata only; no model/client construction.
    from graphconflictbench.cli import dispatch
    from graphconflictbench.cli import parser as cli_parser
    dry_runs = []
    for condition in ("conflict", "control"):
        index = f"indexes/live/smoke-step4-v2-20261115/{condition}"
        run = f"runs/live/smoke-step4-v2-20261115/{condition}"
        assert not (root / index).exists() and not (root / run).exists()
        common = ["--config", str(plan / "real-smoke.v2.yaml"), "--worker-python", adapter.worker_python,
                  "--dataset", str(smoke.root), "--split", "pilot", "--condition", condition]
        for command, tail in (("index", ["--output-dir", index]),
                              ("run", ["--index-dir", index, "--output-dir", run, "--budget", "4096"])):
            dry_runs.append(dispatch(cli_parser().parse_args([command, *common, *tail, "--dry-run"])))
    units = tests(out / "unit-final.xml")
    integration = tests(out / "integration-verified.xml")
    assert (out / "ruff-verified.txt").read_text().strip() == "All checks passed!"
    result = {"date_asia_kolkata": "2026-11-15", "unit_tests": units, "integration_tests": integration,
              "total_passed": units["tests"] + integration["tests"], "ruff": "passed",
              "pilot_audit": validate_dataset(pilot.root, ontology),
              "stratified_audit": validate_dataset(smoke.root, ontology),
              "stratified_record_lineage": "all records and certificates identical to parent pilot",
              "smoke_predicate_case_counts": dict(Counter(c.relation_family for c in smoke.cases)),
              "replayed_prompt_leakage_checks": len(prompt_paths),
              "new_native_prompt_leakage_checks": len(native_prompts),
              "forbidden_metadata_or_gold_field_cases": 0,
              "native_stratified_fixture": fixture, "native_healthcheck": health,
              "implementation_hash": implementation_hash(),
              "historical_archive_files_verified": len(original["sha256"]),
              "historical_archive_sha256": file_hash(out / "historical-step4.zip"),
              "expected_changed_original_source_files": changed,
              "original_data_config_prompt_result_docs_changes": [],
              "previous_readiness_artifact_manifest": "unchanged",
              "prepared_policy": policy.policy.model_dump(), "live_ledger_initialized": False,
              "live_cli_dry_runs": dry_runs, "human_review_decisions": 0,
              "paid_provider_calls": 0,
              "earlier_failed_test_report_preserved": "integration-final.xml: SDK exception expectation corrected; see CHANGE_REPORT.md"}
    write_json(out / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k not in ("live_cli_dry_runs", "prepared_policy")}, indent=2))


if __name__ == "__main__":
    main()
