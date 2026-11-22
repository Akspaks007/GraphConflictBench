"""Verify published LightRAG stores and prepare local CLI index directories."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import yaml

from graphconflictbench.adapters.lightrag_adapter import LightRAGAdapter
from graphconflictbench.manifests import digest, read_jsonl, verify_checksums, write_json

REPO = Path(__file__).resolve().parents[1]


def portable_source_hash():
    root = REPO / "src" / "graphconflictbench"
    return digest({
        path.relative_to(root).as_posix(): hashlib.sha256(
            path.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest()
        for path in root.rglob("*.py")
    })


def portable_config(config):
    return {**config, "provider_control_file": Path(config["provider_control_file"]).name}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-python", required=True)
    parser.add_argument("--output-root", default="indexes/groq-saved")
    args = parser.parse_args()
    config = REPO / "configs" / "architectures" / "lightrag-groq.yaml"
    raw_config = yaml.safe_load(config.read_bytes())
    if not Path(raw_config["provider_control_file"]).is_file():
        parser.error("run from the GraphConflictBench repository root")
    adapter = LightRAGAdapter(config, args.worker_python)
    metadata = adapter.metadata()
    runtime = adapter.healthcheck()["native"]
    source_hash = portable_source_hash()
    archive = REPO / "indexed_graphs" / "groq-pilot"
    output = Path(args.output_root)
    if output.exists():
        parser.error("choose a fresh output root")

    snapshots = {}
    for condition in ("conflict", "control"):
        source = archive / condition
        record = json.loads((source / "snapshot_manifest.json").read_bytes())
        verify_checksums(source, record["checksums"])
        if (record["condition"] != condition or record["native"] != runtime
                or record["source_sha256"] != source_hash
                or record["config"] != portable_config(metadata["config"])):
            raise ValueError(f"{condition} snapshot requires the matching source, config and runtime")
        model = record["embedding_cache"]
        cache = REPO / ".venv-lightrag" / "fastembed-cache" / model["directory"]
        if (cache / "refs" / "main").read_text().strip() != model["revision"]:
            raise ValueError("local BGE model revision differs from the indexed model")
        verify_checksums(cache / "snapshots" / model["revision"], model["checksums"])
        corpus = read_jsonl(source / "corpus.jsonl")
        if digest(corpus) != record["corpus_hash"] or len(corpus) != record["documents_processed"]:
            raise ValueError(f"{condition} corpus differs from the indexed documents")
        snapshots[condition] = record

    for condition, record in snapshots.items():
        source = archive / condition
        index_dir = output / condition
        index_dir.mkdir(parents=True, exist_ok=False)
        for name in record["checksums"]:
            dest = index_dir / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, dest)
        verify_checksums(index_dir, record["checksums"])
        identity = {**metadata, "native": runtime, "condition": condition, "split": record["split"],
                    "corpus_hash": record["corpus_hash"]}
        write_json(index_dir / "index_manifest.json", {
            "schema_version": "1.0", "architecture": "lightrag", "status": "complete",
            "identity": identity, "index_key": digest(identity), "build_result": record["build_result"],
            "checksums": record["checksums"],
        })
        print(f"{condition}: verified {record['documents_processed']} documents in {index_dir}")


if __name__ == "__main__":
    main()
