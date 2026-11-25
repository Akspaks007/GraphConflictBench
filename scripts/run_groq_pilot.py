"""Build both Groq pilot indexes in batches and resume per-case scoring."""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from report_pilot_by_hop import report_pilot

from graphconflictbench.environment import groq_key_pool, load_environment
from graphconflictbench.manifests import verify_checksums, write_json
from graphconflictbench.provider_control import ProviderControl

POLICY = "configs/architectures/groq-policy.json"


def verify_bge_cache(repo):
    snapshot = repo / "indexed_graphs/groq-pilot/conflict/snapshot_manifest.json"
    model = json.loads(snapshot.read_bytes())["embedding_cache"]
    cache = repo / ".venv-lightrag/fastembed-cache" / model["directory"]
    ref = cache / "refs/main"
    if not ref.is_file():
        raise ValueError(f"pinned local BGE cache is missing: {cache}")
    if ref.read_text().strip() != model["revision"]:
        raise ValueError("local BGE model revision differs from the LightRAG baseline")
    verify_checksums(cache / "snapshots" / model["revision"], model["checksums"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--arch", choices=("lightrag", "hipporag2", "pathrag", "microsoft_graphrag"),
        default="lightrag",
    )
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--key-interval-seconds", type=int, default=30, choices=range(1, 61))
    parser.add_argument("--query-key-interval-seconds", type=int, default=60, choices=range(1, 61))
    parser.add_argument("--evidence-budget", type=int)
    parser.add_argument("--key-slot", type=int, help="1-based configured Groq key to start with")
    parser.add_argument(
        "--rotate-on-quota", action="store_true",
        help="resume on the next configured key after a captured 429 and its Retry-After",
    )
    parser.add_argument("--dry-run", action="store_true", help="print the pilot settings offline")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    baseline = args.arch == "lightrag"
    config = f"configs/architectures/{args.arch}-groq.yaml"
    root = args.output_root or Path(
        "runs/groq-pilot-checkpointed" if baseline else f"runs/{args.arch}-groq-pilot"
    )
    budget = args.evidence_budget if args.evidence_budget is not None else (4096 if baseline else 3072)
    if ((args.batch_size is not None and args.batch_size <= 0)
            or budget <= 0 or (args.key_slot is not None and args.key_slot < 1)):
        parser.error("batch size, evidence budget and key slot must be positive")
    if args.arch == "microsoft_graphrag":
        if args.batch_size is not None:
            parser.error("Microsoft GraphRAG builds communities over the complete corpus")
        if budget != 3072:
            parser.error("Microsoft GraphRAG uses the 3,072-token pilot evidence budget")
    elif args.batch_size is None:
        args.batch_size = 10
    slot = args.key_slot or (1 if args.rotate_on_quota else None)
    results = root / ("results" if budget == 4096 else f"results-{budget}")
    if args.dry_run:
        print(json.dumps({
            "arch": args.arch, "config": config, "dataset": "data/generated/pilot",
            "prompt": "configs/prompts/shared_generation.txt", "indexes": str(root / "indexes"),
            "results": str(results), "worker_python": sys.executable,
            "batch_size": args.batch_size, "evidence_budget": budget,
            "conditions": ["conflict", "control"], "key_slot": slot,
            "rotate_on_quota": args.rotate_on_quota,
            "index_key_interval_seconds": args.key_interval_seconds,
            "query_key_interval_seconds": args.query_key_interval_seconds,
        }, indent=2))
        return

    if not baseline:
        verify_bge_cache(repo)
    load_environment()
    env = os.environ.copy()
    keys = groq_key_pool() or (env.get("GROQ_API_KEY"),)
    if slot is not None and (slot > len(keys) or not keys[slot - 1]):
        parser.error("selected Groq key slot is not configured")
    env["PYTHONUTF8"] = "1"
    env.setdefault("TIKTOKEN_CACHE_DIR", str(repo / ".venv" / "tokenizer-cache"))
    while True:
        if slot is not None:
            env["GROQ_API_KEY"] = keys[slot - 1]
            env["GROQ_API_KEYS"] = ""
        try:
            run_pilot(args, repo, config, root, results, budget, env)
        except subprocess.CalledProcessError:
            if not args.rotate_on_quota or not recover_after_quota(repo):
                raise
            slot = slot % len(keys) + 1
            print(f"Retry-After elapsed. Resuming with Groq key slot {slot}.", flush=True)
        else:
            return


def recover_after_quota(repo):
    control = ProviderControl(repo / POLICY)
    if not control.status()["frozen"]:
        return False
    notified = False
    while True:
        try:
            control.recover_groq_rate_limit()
            return True
        except ValueError as error:
            if str(error) != "Groq Retry-After interval has not elapsed":
                raise
            if not notified:
                print("Captured Groq HTTP 429. Waiting for Retry-After before resuming.", flush=True)
                notified = True
            time.sleep(15)


def run_pilot(args, repo, config, root, results, budget, env):
    cli = [sys.executable, "-B", "-m", "graphconflictbench.cli"]
    common = ["--arch", args.arch, "--config", config,
              "--worker-python", sys.executable, "--resume"]
    verify = [*cli, "provider-control", "verify", "--policy", POLICY]
    subprocess.run(verify, cwd=repo, env=env, check=True)
    batch = ["--batch-size", str(args.batch_size)] if args.batch_size is not None else []

    for condition in ("conflict", "control"):
        env["GCB_GROQ_MIN_KEY_INTERVAL_SECONDS"] = str(args.key_interval_seconds)
        index = str(root / "indexes" / condition)
        while True:
            print(f"Indexing {condition}" + (" batch" if batch else ""), flush=True)
            result = subprocess.run(
                [*cli, "index", *common, "--condition", condition, "--output-dir", index,
                 *batch],
                cwd=repo, env=env, check=True, stdout=subprocess.PIPE, encoding="utf-8",
            )
            print(result.stdout, end="", flush=True)
            status = json.loads(result.stdout)["status"]
            if status == "complete":
                break
            if status != "partial":
                raise RuntimeError(f"Unexpected index status for {condition}: {status}")
        print(f"Scoring {condition}", flush=True)
        env["GCB_GROQ_MIN_KEY_INTERVAL_SECONDS"] = str(args.query_key_interval_seconds)
        subprocess.run(
            [*cli, "run", *common, "--condition", condition, "--index-dir", index,
             "--budget", str(budget), "--output-dir", str(results / condition)],
            cwd=repo, env=env, check=True,
        )
        subprocess.run(verify, cwd=repo, env=env, check=True)
    write_json(repo / results / "results_by_hop.json", report_pilot(repo / results))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        sys.exit(f"error: {error}")
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
