"""CLI for the implemented Step 1–4 scope; unsupported architectures fail early."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import yaml

from .adapters.lightrag_adapter import LightRAGAdapter
from .environment import load_environment, redact
from .gemini_control import GeminiControl
from .generator import save_dataset
from .manifests import write_json
from .provider_control import ProviderControl
from .reasoner import Ontology
from .runner import run
from .validator import validate_dataset


def parser():
    p = argparse.ArgumentParser(
        description="GraphConflictBench through native LightRAG integration"
    )
    sub = p.add_subparsers(dest="command", required=True)
    ontology = sub.add_parser("validate-ontology", help="validate declared relation semantics")
    ontology.add_argument("--config", default="configs/ontology.yaml")
    gen = sub.add_parser("generate", help="write a deterministic paired dataset")
    gen.add_argument("--size", choices=["smoke", "pilot", "full", "handbook-full"], default="pilot")
    gen.add_argument("--families", type=int)
    gen.add_argument("--config", default="configs/experiment.yaml")
    gen.add_argument("--seed", type=int, default=None)
    gen.add_argument("--ontology", default="configs/ontology.yaml")
    gen.add_argument("--output-dir")
    gen.add_argument("--resume", action="store_true")
    audit = sub.add_parser("audit", help="verify hashes, provenance, logic and condition isolation")
    audit.add_argument("--dataset", default="data/generated/pilot")
    audit.add_argument("--ontology", default="configs/ontology.yaml")
    audit.add_argument("--write-report", action="store_true")
    audit.add_argument("--output-dir", default="results/audit")
    control = sub.add_parser("provider-control", help="offline capture/spending ledger management")
    control.add_argument(
        "action", choices=["init", "status", "verify", "recover-groq-rate-limit"]
    )
    control.add_argument("--policy", required=True)
    gemini = sub.add_parser("gemini-control", help="offline Gemini eligibility/quota ledger management")
    gemini.add_argument("action", choices=["init", "status", "verify"])
    gemini.add_argument("--policy", required=True)
    check = sub.add_parser("gemini-check", help="ONE live Gemini generation request; not a healthcheck")
    check.add_argument("--config", required=True)
    check.add_argument("--output-dir", required=True)
    for name in ("healthcheck", "index", "run", "smoke-adapters"):
        command = sub.add_parser(name)
        command.add_argument("--arch", choices=["lightrag"], default="lightrag")
        command.add_argument("--config", default="configs/architectures/lightrag-fixture.yaml")
        command.add_argument("--worker-python", default=".venv-lightrag/bin/python")
        if name == "healthcheck":
            continue
        command.add_argument("--dataset", default="data/generated/pilot")
        command.add_argument("--split", choices=["pilot", "design", "dev", "test"], default="pilot")
        command.add_argument("--output-dir")
        command.add_argument("--resume", action="store_true")
        command.add_argument("--ontology", default="configs/ontology.yaml")
        if name in ("index", "run"):
            command.add_argument("--condition", choices=["conflict", "control"], required=True)
        if name == "index":
            command.add_argument("--batch-size", type=int, help="Index one checkpointed batch")
        if name == "run":
            command.add_argument("--index-dir", required=True)
        if name in ("run", "smoke-adapters"):
            command.add_argument("--limit", type=int)
            command.add_argument("--budget", type=int)
            command.add_argument("--prompt", default="configs/prompts/shared_generation.txt")
    for command in sub.choices.values():
        command.add_argument(
            "--dry-run", action="store_true", help="print selected work without writes/calls"
        )
    return p


def dispatch(args):
    if args.dry_run:
        return {"dry_run": True, "plan": vars(args)}
    if args.command == "validate-ontology":
        rules = Ontology.load(args.config)
        return {"status": "valid", "relations": list(rules.relations)}
    if args.command == "provider-control":
        control = ProviderControl(args.policy)
        if args.action == "recover-groq-rate-limit":
            return control.recover_groq_rate_limit()
        return control.initialize() if args.action == "init" else getattr(control, args.action)()
    if args.command == "gemini-control":
        control = GeminiControl(args.policy)
        return control.initialize() if args.action == "init" else getattr(control, args.action)()
    if args.command == "gemini-check":
        return gemini_connectivity(args.config, args.output_dir)
    if args.command == "generate":
        experiment = yaml.safe_load(Path(args.config).read_text())
        families = (
            args.families
            or {
                "smoke": 6,
                "pilot": experiment["pilot_families"],
                "full": experiment["full_families"],
                "handbook-full": experiment["handbook_full_families"],
            }[args.size]
        )
        output = args.output_dir or f"data/generated/{args.size}"
        manifest = save_dataset(
            output,
            Ontology.load(args.ontology),
            families,
            experiment["seed"] if args.seed is None else args.seed,
            pilot=args.size in ("smoke", "pilot"),
            resume=args.resume,
        )
        return {
            "output": output,
            "cases": manifest["case_count"],
            "dataset_hash": manifest["dataset_hash"],
        }
    if args.command == "audit":
        report = validate_dataset(args.dataset, Ontology.load(args.ontology))
        if args.write_report:
            write_json(Path(args.output_dir) / "audit.json", report)
        return report
    adapter = LightRAGAdapter(args.config, args.worker_python)
    if args.command == "healthcheck":
        return adapter.healthcheck()
    ontology = Ontology.load(args.ontology)
    validate_dataset(args.dataset, ontology)
    if args.command == "index":
        output = args.output_dir or f"indexes/lightrag/{args.split}/{args.condition}"
        manifest = adapter.index(
            Path(args.dataset) / "corpora" / args.split / args.condition / "corpus_manifest.json",
            output,
            args.resume,
            args.batch_size,
        )
        return {
            "index_dir": output,
            "index_key": manifest["index_key"],
            "status": manifest["status"],
            **{name: manifest[name] for name in ("documents_processed", "documents_total")
               if name in manifest},
        }
    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be positive")
    budget = args.budget or adapter.config["evidence_budget"]
    if args.command == "run":
        return run(
            adapter,
            args.dataset,
            ontology,
            args.split,
            args.condition,
            args.index_dir,
            args.output_dir or f"runs/lightrag/{args.split}/{args.condition}",
            args.prompt,
            budget,
            args.limit,
            args.resume,
        )
    output = Path(args.output_dir or "results/lightrag-smoke")
    summaries = {}
    for condition in ("conflict", "control"):
        index_dir = output / "indexes" / condition
        adapter.index(
            Path(args.dataset) / "corpora" / args.split / condition / "corpus_manifest.json",
            index_dir,
            args.resume,
        )
        summaries[condition] = run(
            adapter,
            args.dataset,
            ontology,
            args.split,
            condition,
            index_dir,
            output / "runs" / condition,
            args.prompt,
            budget,
            args.limit,
            args.resume,
        )
    write_json(output / "smoke_summary.json", summaries)
    return summaries


def gemini_connectivity(config_file, output_dir):
    from .providers import model_provider

    adapter = LightRAGAdapter(config_file, sys.executable)
    if adapter.config["provider"] != "gemini":
        raise ValueError("gemini-check requires provider=gemini")
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=False)

    async def invoke():
        models = model_provider(adapter.config)
        try:
            text = await models.llm("Reply with exactly OK.")
            assert len(models.usage) == 1
            return {"status": "connected", "requests": 1, "response": redact(text),
                    "usage": models.usage, "benchmark_eligible": False}
        finally:
            await models.client.close()

    try:
        result = asyncio.run(invoke())
        write_json(output / "connectivity.json", result)
        return result
    except Exception as error:
        write_json(output / "error.json", {"type": type(error).__name__, "message": redact(str(error))})
        raise


def main():
    load_environment()
    args = parser().parse_args()
    try:
        print(redact(json.dumps(dispatch(args), indent=2, sort_keys=True)))
    except (ValueError, RuntimeError, OSError, KeyError) as error:
        print(redact(f"error: {error}"), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
