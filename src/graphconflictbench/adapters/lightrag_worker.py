"""Isolated process using the official LightRAG SDK, never the canonical KG."""

import asyncio
import importlib.metadata
import json
import sys
from functools import partial
from pathlib import Path

from ..environment import load_environment, redact
from ..manifests import read_jsonl, write_json
from ..models import fixture_embedding, fixture_llm
from ..providers import model_provider


def native_metadata():
    dist = importlib.metadata.distribution("lightrag-hku")
    direct = json.loads(dist.read_text("direct_url.json") or "{}")
    return {
        "version": dist.version,
        "commit": direct.get("vcs_info", {}).get("commit_id"),
        "url": direct.get("url"),
        "python": sys.version.split()[0],
    }


async def execute(request):
    from lightrag import LightRAG, QueryParam
    from lightrag.base import DocStatus
    from lightrag.utils import EmbeddingFunc

    config = request["config"]
    actual = native_metadata()
    if actual["commit"] != config["upstream_commit"]:
        raise ValueError(f"installed LightRAG commit differs from config: {actual}")
    models = model_provider(config)

    # LightRAG deep-copies its configuration. Functions keep the live client
    # and its non-copyable transport locks outside that snapshot.
    async def provider_llm(*args, **kwargs):
        return await models.llm(*args, **kwargs)

    async def provider_embedding(*args, **kwargs):
        return await models.embedding(*args, **kwargs)

    rag = LightRAG(
        working_dir=str(Path(request["native_dir"]).resolve()),
        llm_model_func=provider_llm if models else fixture_llm,
        llm_model_name=config["llm_model"],
        embedding_func=EmbeddingFunc(
            embedding_dim=config["embedding_dimension"],
            max_token_size={"gemini": 2048, "groq": 512}.get(config["provider"], 8192),
            model_name=config["embedding_model"],
            func=provider_embedding
            if models
            else partial(fixture_embedding, dimension=config["embedding_dimension"]),
        ),
        entity_extract_max_gleaning=config["extract_gleaning"],
        chunk_token_size=config["chunk_token_size"],
        chunk_overlap_token_size=config["chunk_overlap_token_size"],
        llm_model_max_async=config["max_concurrency"],
        embedding_func_max_async=config["max_concurrency"],
        max_parallel_insert=config["max_concurrency"],
        cosine_better_than_threshold=config["cosine_threshold"],
        enable_llm_cache=False,
        enable_llm_cache_for_entity_extract=False,
    )
    await rag.initialize_storages()
    try:
        if request["operation"] == "index":
            docs = read_jsonl(request["corpus_file"])
            await rag.ainsert(
                [d["text"] for d in docs],
                ids=[d["doc_id"] for d in docs],
                file_paths=[d["file_path"] for d in docs],
            )
            failed = await rag.doc_status.get_docs_by_statuses([DocStatus.FAILED], strict=True)
            processed = await rag.doc_status.get_docs_by_statuses(
                [DocStatus.PROCESSED], strict=True
            )
            expected = request.get("expected_document_count", len(docs))
            if failed or len(processed) != expected or any(d["doc_id"] not in processed for d in docs):
                raise RuntimeError(
                    f"native indexing incomplete: processed={len(processed)}, "
                    f"expected={expected}, failed={len(failed)}"
                )
            return {
                "status": "complete",
                "documents_processed": len(processed),
                "native": actual,
                "usage": models.usage if models else [],
            }
        raw = await rag.aquery_data(
            request["query"],
            param=QueryParam(
                mode=config["mode"],
                only_need_context=True,
                top_k=config["top_k"],
                chunk_top_k=config["chunk_top_k"],
                max_total_tokens=config["max_total_tokens"],
                max_entity_tokens=config["max_entity_tokens"],
                max_relation_tokens=config["max_relation_tokens"],
                enable_rerank=False,
            ),
        )
        return {"raw": raw, "native": actual, "usage": models.usage if models else []}
    finally:
        try:
            await rag.finalize_storages()
        finally:
            if models:
                await models.client.close()


def main():
    load_environment()
    request = json.loads(Path(sys.argv[1]).read_text())
    if request["operation"] == "healthcheck":
        result = {"status": "available", "native": native_metadata()}
    else:
        result = asyncio.run(execute(request))
    write_json(request["response_file"], result)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(redact(f"{type(error).__name__}: {error}"), file=sys.stderr)
        sys.exit(1)
