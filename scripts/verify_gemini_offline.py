"""Verify public Gemini integration artifacts without calling any provider.

Private .env files are never copied, hashed or included in reports. Known
credentials are used only in memory for a boolean artifact-redaction check.
"""

import argparse
import json
import platform
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter, implementation_hash
from graphconflictbench.environment import load_environment, redact_bytes
from graphconflictbench.gemini_control import GeminiControl, GeminiError
from graphconflictbench.manifests import file_hash, verify_checksums, write_json
from graphconflictbench.prompts import GRAPH_FIELDS, build_prompt
from graphconflictbench.reasoner import Ontology
from graphconflictbench.runner import normalize
from graphconflictbench.validator import Dataset, validate_dataset


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from all_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from all_keys(item)


def test_counts(path):
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
    if (out / "verification-release.json").exists():
        raise ValueError("verification already exists; use a new version")
    load_environment()
    baseline = load(root / "results/step4-validity-v2-20261115/V2_MANIFEST.json")
    historical = {p: h for p, h in baseline["sha256"].items()
                  if p.startswith(("data/", "results/"))}
    verify_checksums(root, historical)
    unchanged = ["src/graphconflictbench/models.py", "src/graphconflictbench/provider_control.py",
                 "src/graphconflictbench/prompts.py", "src/graphconflictbench/metrics.py",
                 "src/graphconflictbench/evidence_mapper.py", "src/graphconflictbench/reasoner.py",
                 "src/graphconflictbench/runner.py", "src/graphconflictbench/schemas.py",
                 "configs/prompts/shared_generation.txt", "configs/ontology.yaml"]
    with zipfile.ZipFile(out / "step4-v2-code-baseline.zip") as archive:
        assert all(archive.read(p) == (root / p).read_bytes() for p in unchanged)
        assert archive.read(".gitignore") == (root / ".gitignore").read_bytes()
        assert not any(Path(n).name == ".env" for n in archive.namelist())
    ds = Dataset(root / "data/generated/pilot")
    ontology = Ontology.load(root / "configs/ontology.yaml")
    forbidden = {"created_at", "build_id", "source_id", "gold_label", "gold_proof_sets",
                 "gold_conflict_pairs", "mapped_assertion_ids", "condition", "family_id", "hop_depth"}

    def check_prompt(text):
        payload = json.loads(text)
        assert not set(all_keys(payload)) & forbidden
        assert not re.search(r"\bE[0-9a-f]{20}\b", text)
        for kind, rows in payload["evidence"]["native_graph"].items():
            assert all(set(row) <= set(GRAPH_FIELDS[kind]) for row in rows)

    rebuilt = 0
    for case in ds.cases:
        path = root / "results/lightrag-pilot/runs" / case.condition / "cases" / case.case_id / "native-1/response.json"
        raw = load(path)["raw"]
        retrieval = normalize(raw, ds, case, "gemini_offline_presentation_check", 0.0, 4096, False)
        system, prompt, hashed = build_prompt(case, retrieval, ontology,
                                             root / "configs/prompts/shared_generation.txt")
        check_prompt(prompt)
        previous = load(root / "results/step4-validity-v2-20261115/final-plan/prompt-replay-v2" / case.case_id / "prompt.json")
        assert hashed == previous["hash"] and prompt == previous["prompt"]
        record = {
            "kind": "offline_replay_not_provider_execution", "system": system,
            "prompt": prompt, "hash": hashed, "raw_response_sha256": file_hash(path),
        }
        destination = out / "leakage-replay-release" / case.case_id / "prompt.json"
        if destination.exists():
            assert load(destination) == record
        else:
            write_json(destination, record)
        rebuilt += 1
    native_root = out / "offline-integration-release"
    # Pytest's Windows 'current' junctions alias the numbered test directories.
    native_prompts = sorted({p.resolve() for p in native_root.glob("*/runs/*/cases/*/prompt.json")})
    for path in native_prompts:
        check_prompt(load(path)["prompt"])
    gemini_callback_prompts = 0
    for path in sorted({p.resolve() for p in native_root.glob("*/capture/requests/*/request.body")}):
        payload = load(path)
        if "contents" not in payload:
            continue
        text = payload["contents"][-1]["parts"][0]["text"]
        if text.startswith('{"case_id":'):
            check_prompt(text)
            assert payload["systemInstruction"]["parts"][0]["text"] == (root / "configs/prompts/shared_generation.txt").read_text(encoding="utf-8")
            gemini_callback_prompts += 1
    assert gemini_callback_prompts == 12
    assert len(native_prompts) == 24
    plan = out / "proposed-plan-v3"
    adapter = LightRAGAdapter(plan / "lightrag-gemini.yaml", root / ".venv-lightrag/Scripts/python.exe")
    guard = GeminiControl(adapter.config["provider_control_file"], adapter.config["provider_control_sha256"])
    assert not guard.root.exists()
    try:
        guard.require_eligibility()
    except GeminiError:
        pass
    else:
        raise AssertionError("the unverified proposed live plan must stay blocked")
    for condition in ("conflict", "control"):
        assert not (root / "indexes/gemini/stratified-v1-20261115" / condition).exists()
        assert not (root / "runs/gemini/stratified-v1-20261115" / condition).exists()
    public = [p for p in out.rglob("*") if p.is_file() and p.suffix != ".zip"
              and not (p.name == ".env" or p.name.startswith(".env."))]
    for path in public:
        data = path.read_bytes()
        if redact_bytes(data) != data:
            raise AssertionError("configured credential detected in a public artifact; values suppressed")
    units = test_counts(out / "unit-release.xml")
    integration = test_counts(out / "integration-release.xml")
    assert (out / "ruff-release.txt").read_text().strip() == "All checks passed!"
    result = {
        "date_asia_kolkata": "2026-11-15", "python": platform.python_version(),
        "unit_tests": units, "integration_tests": integration,
        "total_passed": units["tests"] + integration["tests"], "ruff": "passed",
        "pilot_audit": validate_dataset(ds.root, ontology),
        "stratified_smoke_audit": validate_dataset(root / "results/step4-validity-v2-20261115/stratified-smoke-v2", ontology),
        "unchanged_openai_v2_research_files": unchanged,
        "historical_data_result_files_verified_unchanged": len(historical),
        "metadata_leakage_replays": rebuilt, "replay_hashes_match_v2": True,
        "new_native_prompt_leakage_checks": len(native_prompts),
        "gemini_rest_final_generation_shared_prompt_checks": gemini_callback_prompts,
        "known_configured_secrets_in_public_artifacts": False,
        "private_dotenv_files_copied_hashed_or_archived": False,
        "dotenv_runtime_loading": "repository root; override=False; values never reported",
        "dotenv_core_pin": "1.2.4", "dotenv_native_pin_already_present": "1.2.4",
        "gitignore_user_supplied_rules_preserved": True,
        "implementation_hash": implementation_hash(),
        "native_healthcheck": adapter.healthcheck(),
        "project_free_tier_eligibility": "unverified; no project API or billing inquiry",
        "live_gemini_requests": 0, "billing_enabled_or_modified": False,
        "proposed_live_ledger_initialized": False, "original_pilot_regenerated": False,
        "earlier_failed_native_attempt_preserved": "gemini-native-first; callback-copy semantics fixed before passing reruns",
    }
    write_json(out / "verification-release.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
