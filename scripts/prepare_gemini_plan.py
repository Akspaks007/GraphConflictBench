"""Prepare an immutable optional Gemini plan offline; never writes a credential.

Attestation flags are manual declarations from project settings, not API checks.
No source data, labels or shared prompts are regenerated or changed.
"""

import argparse
import sys
from pathlib import Path

import yaml

from graphconflictbench.adapters.lightrag_adapter import implementation_hash
from graphconflictbench.environment import load_environment, redact
from graphconflictbench.gemini_control import GeminiControl, GeminiPolicy
from graphconflictbench.manifests import canonical, file_hash, write_json


def main():
    load_environment()  # Only for safe redaction; no credential value enters a plan.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--eligibility-status", choices=["unverified", "free-tier-confirmed", "paid-tier-confirmed"], default="unverified")
    parser.add_argument("--eligibility-reference", default="")
    parser.add_argument("--eligibility-checked-on", default="")
    parser.add_argument("--quotas-reviewed", action="store_true")
    parser.add_argument("--max-requests", type=int, default=500)
    parser.add_argument("--max-requests-per-24h", type=int, default=200)
    parser.add_argument("--min-interval-seconds", type=int, default=31)
    parser.add_argument("--max-input-tokens-per-minute", type=int, default=40000)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    policy = GeminiPolicy(state_directory="gemini-control-v1", eligibility_status=args.eligibility_status,
                          eligibility_reference=args.eligibility_reference,
                          eligibility_checked_on=args.eligibility_checked_on,
                          quotas_reviewed=args.quotas_reviewed, max_requests=args.max_requests,
                          max_requests_per_24h=args.max_requests_per_24h,
                          min_interval_seconds=args.min_interval_seconds,
                          max_input_tokens_per_minute=args.max_input_tokens_per_minute)
    if redact(canonical(policy.model_dump())) != canonical(policy.model_dump()):
        raise ValueError("A Gemini attestation/plan must not contain a credential")
    policy_file = out / "gemini-policy.json"
    write_json(policy_file, policy.model_dump())
    if policy.eligibility_status != "unverified":
        GeminiControl(policy_file).require_eligibility()
    config = yaml.safe_load(Path("configs/architectures/lightrag-gemini.yaml").read_text())
    config.update(provider_control_file=policy_file.as_posix(), provider_control_sha256=file_hash(policy_file))
    (out / "lightrag-gemini.yaml").write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    write_json(out / "plan.json", {"provider": "gemini", "live_requests_executed": 0,
                                  "eligibility_status": policy.eligibility_status,
                                  "implementation_hash": implementation_hash(),
                                  "dataset": "results/step4-validity-v2-20261115/stratified-smoke-v2",
                                  "shared_prompt_sha256": file_hash("configs/prompts/shared_generation.txt"),
                                  "policy_sha256": file_hash(policy_file)})
    print("Prepared a new Gemini plan; no credential stored and no API request made.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(redact(f"error: {error}"), file=sys.stderr)
        sys.exit(1)
