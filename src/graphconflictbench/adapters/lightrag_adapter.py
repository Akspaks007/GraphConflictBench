"""Native SDK subprocess adapter; immutable, condition-isolated snapshots."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, model_validator

from ..manifests import (
    digest,
    exclusive_lock,
    file_hash,
    read_jsonl,
    tree_checksums,
    verify_checksums,
    write_json,
    write_jsonl,
)
from ..schemas import Record


class AdapterConfig(Record):
    architecture: Literal["lightrag"]
    provider: Literal["fixture", "openai", "gemini", "groq"]
    upstream_repository: str
    upstream_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    upstream_license: str
    python: str
    mode: Literal["hybrid", "mix", "local", "global"]
    llm_model: str
    embedding_model: str
    embedding_dimension: int = Field(gt=0)
    top_k: int = Field(gt=0)
    chunk_top_k: int = Field(gt=0)
    max_total_tokens: int = Field(gt=0)
    max_entity_tokens: int = Field(gt=0)
    max_relation_tokens: int = Field(gt=0)
    evidence_budget: int = Field(gt=0)
    chunk_token_size: int = Field(gt=0)
    chunk_overlap_token_size: int = Field(ge=0)
    max_concurrency: int = Field(gt=0)
    max_retries: int = Field(ge=0)
    extract_gleaning: int = Field(ge=0)
    cosine_threshold: float
    benchmark_eligible: bool
    provider_control_file: str | None = None
    provider_control_sha256: str | None = None
    embedding_task_type: Literal["SEMANTIC_SIMILARITY"] | None = None

    @model_validator(mode="after")
    def provider_configuration(self):
        if self.provider == "gemini":
            if self.llm_model != "gemini-2.5-flash" or self.embedding_model != "gemini-embedding-001":
                raise ValueError("Gemini model substitution requires a reviewed integration change")
            if self.embedding_dimension not in (768, 1536, 3072):
                raise ValueError("use a reviewed Gemini embedding dimension: 768, 1536 or 3072")
            if self.embedding_task_type != "SEMANTIC_SIMILARITY":
                raise ValueError("Gemini requires the same SEMANTIC_SIMILARITY task for every embedding")
            if self.max_retries != 0 or self.max_concurrency != 1:
                raise ValueError("Gemini smoke requires zero retries and concurrency one")
            if self.benchmark_eligible:
                raise ValueError("Gemini readiness smoke is not benchmark eligible")
        if self.provider == "groq":
            if self.embedding_model != "BAAI/bge-small-en-v1.5" or self.embedding_dimension != 384:
                raise ValueError("Groq requires the configured 384-dimensional local BGE model")
            if self.max_retries != 0 or self.max_concurrency != 1 or self.benchmark_eligible:
                raise ValueError("Groq smoke requires zero retries and concurrency one")
        return self


def implementation_hash():
    root = Path(__file__).resolve().parents[1]
    return digest({str(p.relative_to(root)): file_hash(p) for p in sorted(root.rglob("*.py"))})


class LightRAGAdapter:
    def __init__(self, config, worker_python):
        self.config = AdapterConfig.model_validate(
            yaml.safe_load(Path(config).read_text())
        ).model_dump()
        if self.config["provider"] == "fixture" and self.config["benchmark_eligible"]:
            raise ValueError("fixture models cannot be benchmark eligible")
        if self.config["provider_control_file"]:
            policy = Path(self.config["provider_control_file"]).resolve()
            if not self.config["provider_control_sha256"]:
                raise ValueError("provider control policy requires its frozen SHA256")
            if file_hash(policy) != self.config["provider_control_sha256"]:
                raise ValueError("provider control policy checksum changed")
            self.config["provider_control_file"] = str(policy)
        # Resolving a venv's python symlink selects the base interpreter and loses isolation.
        self.worker_python = str(Path(worker_python).absolute())

    def _worker_timeout(self, operation):
        if self.config["provider"] != "gemini" or operation == "healthcheck":
            return 1800
        from ..gemini_control import GeminiControl

        if not self.config["provider_control_file"]:
            raise ValueError("Gemini requires a frozen quota policy before worker execution")
        policy = GeminiControl(self.config["provider_control_file"],
                               self.config["provider_control_sha256"]).policy
        # Slow quota-compliant indexing must not hit the existing 30-minute limit.
        # This is process headroom, not extra permission to dispatch: the shared
        # lifetime/day/spend/deadline guards still stop requests independently.
        calls = min(policy.max_requests, policy.max_requests_per_24h)
        return 1800 + calls * (policy.min_interval_seconds + 180)

    def _call(self, operation, directory, **kwargs):
        directory = Path(directory).resolve()
        try:
            directory.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            raise ValueError("native trace directory exists; use a fresh attempt path") from None
        request_path, response_path = directory / "request.json", directory / "response.json"
        write_json(
            request_path,
            {
                "operation": operation,
                "config": self.config,
                "response_file": str(response_path),
                **kwargs,
            },
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
        with (directory / "native.log").open("w") as log:
            result = subprocess.run(
                [
                    self.worker_python,
                    "-m",
                    "graphconflictbench.adapters.lightrag_worker",
                    str(request_path),
                ],
                env=env,
                cwd=directory,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=self._worker_timeout(operation),
            )
        if result.returncode:
            raise RuntimeError(f"LightRAG worker failed; inspect {directory / 'native.log'}")
        if not response_path.exists():
            raise RuntimeError("LightRAG worker returned no response")
        return json.loads(response_path.read_text())

    def healthcheck(self):
        tmp = tempfile.mkdtemp(prefix="gcb-health-")
        result = self._call("healthcheck", Path(tmp) / "trace")
        shutil.rmtree(tmp)
        if result["native"]["commit"] != self.config["upstream_commit"]:
            raise ValueError("worker has an unexpected upstream commit")
        return result

    def metadata(self):
        return {
            "config": self.config,
            "config_hash": digest(self.config),
            "implementation_hash": implementation_hash(),
        }

    def index(self, corpus_manifest, index_dir, resume=False, batch_size=None):
        if batch_size is not None and batch_size <= 0:
            raise ValueError("index batch size must be positive")
        corpus_manifest = Path(corpus_manifest).resolve()
        cm = json.loads(corpus_manifest.read_text())
        if cm["condition"] not in ("conflict", "control"):
            raise ValueError("each index must have exactly one condition")
        rows = read_jsonl(corpus_manifest.parent / cm["documents_file"])
        if cm["document_count"] != len(rows) or cm["corpus_hash"] != digest(rows):
            raise ValueError("corpus hash/count mismatch")
        if len({x["doc_id"] for x in rows}) != len(rows):
            raise ValueError("duplicate corpus document ID")
        if any(set(x) != {"doc_id", "text", "file_path"} for x in rows):
            raise ValueError("only raw documents and neutral source IDs may reach native indexing")
        identity = {
            "corpus_hash": cm["corpus_hash"],
            "split": cm["split"],
            "condition": cm["condition"],
            **self.metadata(),
            "native": self.healthcheck()["native"],
        }
        index_dir = Path(index_dir).resolve()
        with exclusive_lock(index_dir):
            saved = index_dir / "index_manifest.json"
            if saved.exists():
                manifest = json.loads(saved.read_text())
                if not resume or manifest["identity"] != identity:
                    raise ValueError("index exists or cache identity changed; use a new directory")
                verify_checksums(index_dir, manifest["checksums"])
                return manifest
            if batch_size is not None:
                return self._index_batch(index_dir, identity, rows, batch_size, resume)
            if any(p.name != ".job.lock" for p in index_dir.iterdir()):
                raise ValueError(
                    "incomplete index directory; use a fresh path after inspecting logs"
                )
            write_jsonl(index_dir / "corpus.jsonl", rows)
            native_dir = index_dir / "native"
            result = self._call(
                "index",
                index_dir / "build",
                native_dir=str(native_dir),
                corpus_file=str(index_dir / "corpus.jsonl"),
            )
            manifest = {
                "schema_version": "1.0",
                "architecture": "lightrag",
                "status": "complete",
                "identity": identity,
                "index_key": digest(identity),
                "build_result": result,
                "checksums": tree_checksums(index_dir, exclude=("index_manifest.json",)),
            }
            write_json(saved, manifest)
            return manifest

    def _index_batch(self, index_dir, identity, rows, batch_size, resume):
        path = index_dir / "index_checkpoint.json"
        corpus = index_dir / "corpus.jsonl"
        if path.exists():
            checkpoint = json.loads(path.read_bytes())
            if not resume or checkpoint["identity"] != identity or digest(read_jsonl(corpus)) != digest(rows):
                raise ValueError("index checkpoint differs or --resume was omitted")
        else:
            if any(p.name != ".job.lock" for p in index_dir.iterdir()):
                raise ValueError("existing index directory has no batch checkpoint")
            write_jsonl(corpus, rows)
            checkpoint = {"identity": identity, "documents_processed": 0}
            write_json(path, checkpoint)

        done = checkpoint["documents_processed"]
        previous = index_dir / checkpoint["batch"] / "native" if done else None
        if previous:
            verify_checksums(previous, checkpoint["checksums"])
        if done < len(rows):
            staging = index_dir / "batches"
            staging.mkdir(exist_ok=True)
            attempt = Path(tempfile.mkdtemp(prefix=f"{done:04d}-", dir=staging))
            native = attempt / "native"
            if previous:
                shutil.copytree(previous, native)
            batch = rows[done:done + batch_size]
            write_jsonl(attempt / "corpus.jsonl", batch)
            build = self._call("index", attempt / "build", native_dir=str(native),
                               corpus_file=str(attempt / "corpus.jsonl"),
                               expected_document_count=done + len(batch))
            done = build["documents_processed"]
            checkpoint = {"identity": identity, "documents_processed": done,
                          "batch": attempt.relative_to(index_dir).as_posix(),
                          "checksums": tree_checksums(native)}
            write_json(path, checkpoint)
            previous = native
        result = {"status": "partial", "index_key": digest(identity),
                  "documents_processed": done, "documents_total": len(rows)}
        if done < len(rows):
            return result
        native = index_dir / "native"
        if not native.exists():
            temporary = Path(tempfile.mkdtemp(prefix="finalize-", dir=index_dir / "batches"))
            shutil.copytree(previous, temporary / "native")
            (temporary / "native").rename(native)
        verify_checksums(native, checkpoint["checksums"])
        manifest = {
            **result, "schema_version": "1.0", "architecture": "lightrag",
            "identity": identity, "status": "complete",
            "build_result": {"status": "complete", "documents_processed": done,
                             "native": identity["native"], "usage": []},
            "checksums": tree_checksums(index_dir, exclude=("index_manifest.json",)),
        }
        write_json(index_dir / "index_manifest.json", manifest)
        return manifest

    def retrieve(self, query, index_dir, budget=4096, trace=True, trace_dir=None):
        if not trace:
            raise ValueError("trace capture is mandatory for this benchmark")
        if budget <= 0:
            raise ValueError("evidence budget must be positive")
        index_dir = Path(index_dir).resolve()
        manifest = json.loads((index_dir / "index_manifest.json").read_text())
        expected = self.metadata()
        if any(manifest["identity"][k] != v for k, v in expected.items()):
            raise ValueError("configuration or implementation differs from indexed snapshot")
        verify_checksums(index_dir, manifest["checksums"])
        # Retrieval can update keyword caches. Query a copy so the snapshot stays immutable.
        with tempfile.TemporaryDirectory(prefix="gcb-query-") as tmp:
            clone = Path(tmp) / "native"
            shutil.copytree(index_dir / "native", clone)
            destination = Path(trace_dir) if trace_dir else Path(tmp) / "trace"
            result = self._call("retrieve", destination, native_dir=str(clone), query=query)
        if result["native"] != manifest["identity"]["native"]:
            raise ValueError("native worker version changed since indexing")
        return result
