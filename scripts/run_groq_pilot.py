"""Build both Groq pilot indexes in batches and resume per-case scoring."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default="runs/groq-pilot-checkpointed")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--key-interval-seconds", type=int, default=30, choices=range(1, 61))
    parser.add_argument("--query-key-interval-seconds", type=int, default=60, choices=range(1, 61))
    parser.add_argument("--evidence-budget", type=int, default=4096)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env.setdefault("TIKTOKEN_CACHE_DIR", str(repo / ".venv" / "tokenizer-cache"))
    cli = [sys.executable, "-B", "-m", "graphconflictbench.cli"]
    common = ["--config", "configs/architectures/lightrag-groq.yaml",
              "--worker-python", sys.executable, "--resume"]
    root = Path(args.output_root)

    for condition in ("conflict", "control"):
        env["GCB_GROQ_MIN_KEY_INTERVAL_SECONDS"] = str(args.key_interval_seconds)
        index = str(root / "indexes" / condition)
        while True:
            print(f"Indexing {condition} batch", flush=True)
            result = subprocess.run(
                [*cli, "index", *common, "--condition", condition, "--output-dir", index,
                 "--batch-size", str(args.batch_size)],
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
        results = "results" if args.evidence_budget == 4096 else f"results-{args.evidence_budget}"
        subprocess.run(
            [*cli, "run", *common, "--condition", condition, "--index-dir", index,
             "--budget", str(args.evidence_budget), "--output-dir", str(root / results / condition)],
            cwd=repo, env=env, check=True,
        )
        subprocess.run(
            [*cli, "provider-control", "verify", "--policy", "configs/architectures/groq-policy.json"],
            cwd=repo, env=env, check=True,
        )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
