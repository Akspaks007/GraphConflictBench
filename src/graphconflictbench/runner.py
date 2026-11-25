"""Resumable per-case native retrieval and JSON generation, with immutable traces."""

import json
import time
from pathlib import Path

import tiktoken

from .adapters.base import implementation_hash
from .evidence_mapper import map_chunk
from .inference import generate_prediction, serialize_prediction
from .manifests import (
    canonical,
    digest,
    exclusive_lock,
    file_hash,
    tree_checksums,
    verify_checksums,
    write_json,
    write_jsonl,
)
from .metrics import aggregate, score_case
from .prompts import build_prompt, evidence_envelope, model_visible_graph
from .schemas import Retrieval
from .validator import Dataset


def normalize(raw, dataset, case, run_id, elapsed, budget, eligible, *, architecture="lightrag"):
    encoder = tiktoken.get_encoding("cl100k_base")
    payload = raw.get("data", {})
    visible_graph = model_visible_graph(payload)
    items, graph = [], {"entities": [], "relationships": [], "references": []}
    retrieval = Retrieval(
        run_id=run_id,
        architecture=architecture,
        case_id=case.case_id,
        retrieval_ms=elapsed,
        context_tokens=0,
        retrieved_items=items,
        capture_complete=True,
        native_status=raw.get("status", "unknown"),
        adapter_warnings=[],
        benchmark_eligible=eligible,
        native_graph=graph,
    )
    for chunk in payload.get("chunks", []):
        item = map_chunk(
            chunk, dataset.documents, dataset.assertions, len(retrieval.retrieved_items) + 1
        )
        retrieval.retrieved_items.append(item)
        tokens = len(encoder.encode(canonical(evidence_envelope(retrieval))))
        if tokens > budget:
            retrieval.retrieved_items.pop()
            retrieval.adapter_warnings.append("source_chunk_omitted_by_envelope_budget")
    for name in graph:
        for row in visible_graph[name]:
            retrieval.native_graph[name].append(row)
            if len(encoder.encode(canonical(evidence_envelope(retrieval)))) > budget:
                retrieval.native_graph[name].pop()
                retrieval.adapter_warnings.append("native_graph_row_omitted_by_envelope_budget")
    if raw.get("status") != "success":
        retrieval.adapter_warnings.append("native_retrieval_returned_no_evidence")
    if any(i.mapping_status == "unmapped" for i in retrieval.retrieved_items):
        retrieval.adapter_warnings.append("some_source_chunks_cannot_be_mapped_exactly")
    retrieval.context_tokens = len(encoder.encode(canonical(evidence_envelope(retrieval))))
    if retrieval.context_tokens > budget:
        raise ValueError("evidence budget smaller than an empty envelope")
    retrieval.adapter_warnings = sorted(set(retrieval.adapter_warnings))
    return retrieval


def run(
    adapter,
    dataset_dir,
    ontology,
    split,
    condition,
    index_dir,
    output,
    prompt_file,
    budget=4096,
    limit=None,
    resume=False,
):
    ds = Dataset(dataset_dir)
    cases = ds.select(split, condition)
    if limit:
        cases = cases[:limit]
    if not cases:
        raise ValueError("no cases selected")
    index = json.loads((Path(index_dir) / "index_manifest.json").read_text())
    if index["architecture"] != adapter.config["architecture"]:
        raise ValueError("requested adapter and index have different architectures")
    if index["identity"]["condition"] != condition or index["identity"]["split"] != split:
        raise ValueError("requested cases and index have different condition/split")
    cm = Path(dataset_dir) / "corpora" / split / condition / "corpus_manifest.json"
    if json.loads(cm.read_text())["corpus_hash"] != index["identity"]["corpus_hash"]:
        raise ValueError("index was built from a different corpus")
    identity = {
        "index_key": index["index_key"],
        "implementation_hash": implementation_hash(),
        "dataset_manifest_hash": file_hash(Path(dataset_dir) / "dataset_manifest.json"),
        "case_ids": [c.case_id for c in cases],
        "budget": budget,
        "prompt_hash": file_hash(prompt_file),
        "config": adapter.config,
        "ontology_hash": digest(ontology.model_dump(mode="json")),
    }
    run_id = digest(identity)[:20]
    output = Path(output)
    with exclusive_lock(output):
        manifest_file = output / "run_manifest.json"
        if manifest_file.exists():
            old = json.loads(manifest_file.read_text())
            if not resume or old["identity"] != identity:
                raise ValueError("run already exists or identity differs")
            if old["status"] == "complete":
                verify_checksums(output, old["checksums"])
                return json.loads((output / "summary.json").read_text())
        elif any(p.name != ".job.lock" for p in output.iterdir()):
            raise ValueError("output directory is not empty")
        write_json(manifest_file, {"status": "running", "run_id": run_id, "identity": identity})
        scores, retrievals, predictions = [], [], []
        for case in cases:
            job = output / "cases" / case.case_id
            marker = job / "complete.json"
            if resume and marker.exists():
                saved = json.loads(marker.read_text())
                verify_checksums(job, saved["checksums"])
                score = json.loads((job / "score.json").read_text())
                retrieval = json.loads((job / "retrieval.json").read_text())
                prediction = json.loads((job / "prediction.json").read_text())
            else:
                if job.exists():
                    # Preserve failed attempts for inspection; fresh numbered trace directory.
                    attempt = len(list(job.glob("native-*"))) + 1
                else:
                    attempt = 1
                started = time.perf_counter()
                result = adapter.retrieve(
                    case.query, index_dir, budget, trace_dir=job / f"native-{attempt}"
                )
                elapsed = (time.perf_counter() - started) * 1000
                r = normalize(
                    result["raw"],
                    ds,
                    case,
                    run_id,
                    elapsed,
                    budget,
                    adapter.config["benchmark_eligible"],
                    architecture=adapter.config["architecture"],
                )
                system, prompt, prompt_hash = build_prompt(case, r, ontology, prompt_file)
                attempt_dir = job / f"attempt-{attempt}"
                prompt_record = {"system": system, "prompt": prompt, "hash": prompt_hash}
                write_json(attempt_dir / "prompt.json", prompt_record)
                write_json(attempt_dir / "retrieval.json", r.model_dump())
                try:
                    raw, p, error, usage = generate_prediction(adapter.config, system, prompt, case, r)
                except BaseException as failure:
                    write_json(attempt_dir / "error.json", {
                        "type": type(failure).__name__, "message": str(failure),
                    })
                    raise
                write_json(
                    job / "prompt.json", prompt_record
                )
                prediction = serialize_prediction(raw, p, error, usage)
                score = score_case(case, r, p, ds.documents, ds.assertions)
                retrieval = r.model_dump()
                write_json(attempt_dir / "prediction.json", prediction)
                write_json(attempt_dir / "score.json", score)
                write_json(job / "retrieval.json", retrieval)
                write_json(job / "prediction.json", prediction)
                write_json(job / "score.json", score)
                write_json(marker, {"checksums": tree_checksums(job, exclude=("complete.json",))})
            scores.append(score)
            retrievals.append(retrieval)
            predictions.append({"case_id": case.case_id, **prediction})
        summary = {
            **aggregate(scores),
            "run_id": run_id,
            "benchmark_eligible": adapter.config["benchmark_eligible"],
            "result_kind": "fixture_integration_check"
            if adapter.config["provider"] == "fixture"
            else "provisional_pilot",
            "tokenizer": "cl100k_base",
            "statistical_evaluation": "not_implemented_in_step_4",
            "role_metric_version": "2.0",
            "role_aware_exact_proof_cases": sum(
                s["role_aware_exact_proof_set"] for s in scores
            ),
        }
        write_jsonl(output / "retrieval.jsonl", retrievals)
        write_jsonl(output / "predictions.jsonl", predictions)
        write_jsonl(output / "scores.jsonl", scores)
        write_json(output / "summary.json", summary)
        write_json(
            manifest_file,
            {
                "status": "complete",
                "run_id": run_id,
                "identity": identity,
                "checksums": tree_checksums(output, exclude=("run_manifest.json",)),
            },
        )
        return summary
