"""Summarize checksum-verified scores for the frozen 48-case paired pilot."""

import argparse
import json
from collections import Counter
from pathlib import Path

from graphconflictbench.manifests import file_hash, read_jsonl, verify_checksums
from graphconflictbench.schemas import Case

REPO = Path(__file__).resolve().parents[1]
CONDITIONS = ("conflict", "control")


def report_pilot(results_root):
    dataset = REPO / "data/generated/pilot"
    manifest_path = dataset / "dataset_manifest.json"
    dataset_hash = file_hash(manifest_path)
    frozen = json.loads(manifest_path.read_bytes())
    verify_checksums(dataset, {"cases.jsonl": frozen["checksums"]["cases.jsonl"]})
    cases = read_jsonl(dataset / "cases.jsonl", Case)
    if len(cases) != 48:
        raise ValueError("the frozen pilot must contain 48 cases")

    rows, runs, common = [], {}, None
    for condition in CONDITIONS:
        directory = Path(results_root) / condition
        manifest = json.loads((directory / "run_manifest.json").read_bytes())
        if manifest["status"] != "complete" or "scores.jsonl" not in manifest["checksums"]:
            raise ValueError(f"{condition} run is incomplete")
        verify_checksums(directory, manifest["checksums"])
        identity = manifest["identity"]
        if identity["dataset_manifest_hash"] != dataset_hash:
            raise ValueError(f"{condition} run used a different pilot manifest")

        scores = read_jsonl(directory / "scores.jsonl")
        depths = {case.case_id: case.hop_depth for case in cases if case.condition == condition}
        score_ids = [score["case_id"] for score in scores]
        if score_ids != identity["case_ids"] or len(score_ids) != 24 or set(score_ids) != depths.keys():
            raise ValueError(f"{condition} scores do not cover all 24 frozen cases")
        settings = {k: v for k, v in identity.items() if k not in ("case_ids", "index_key")}
        if common is not None and settings != common:
            raise ValueError("the paired runs used different evaluation settings")
        common = settings
        runs[condition] = {"run_id": manifest["run_id"], "index_key": identity["index_key"]}

        for hop in (1, 2, 3):
            group = [score for score in scores if depths[score["case_id"]] == hop]
            counts = Counter(score["outcome"] for score in group)
            rows.append({
                "condition": condition,
                "hops": hop,
                "cases": len(group),
                **{name: counts[name] for name in ("tp", "tn", "fp", "fn", "error")},
                "complete_proof_retrieved": (
                    sum(score["complete_proof_retrieved"] is True for score in group)
                    if condition == "conflict" else None
                ),
                "exact_proofs": sum(score["role_aware_exact_proof_set"] for score in group),
            })

    if runs["conflict"]["index_key"] == runs["control"]["index_key"]:
        raise ValueError("the two conditions reference the same index")
    config = common["config"]
    return {
        "architecture": config["architecture"],
        "provider": config["provider"],
        "model": config["llm_model"],
        "embedding_model": config["embedding_model"],
        "benchmark_eligible": config["benchmark_eligible"],
        "evidence_budget": common["budget"],
        "dataset_manifest_sha256": common["dataset_manifest_hash"],
        "prompt_sha256": common["prompt_hash"],
        "implementation_hash": common["implementation_hash"],
        "runs": runs,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_dir", type=Path, help="directory containing both condition runs")
    args = parser.parse_args()
    try:
        report = report_pilot(args.results_dir)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"error: {error}\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
