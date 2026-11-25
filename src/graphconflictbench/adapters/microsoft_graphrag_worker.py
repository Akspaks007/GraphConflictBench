"""Run Microsoft GraphRAG standard indexing and Local Search context retrieval."""

import asyncio
import importlib.metadata
import json
import os
import sys
from pathlib import Path

from ..environment import load_environment, redact
from ..manifests import digest, read_jsonl, write_json
from ..models import fixture_embedding, parse_statements
from ..providers import model_provider

MODEL_TYPE = "graphconflictbench"
NATIVE_TABLES = ("documents", "text_units", "entities", "relationships", "communities",
                 "community_reports")


def native_metadata(config):
    packages = ("graphrag", "graphrag-llm", "graphrag-vectors", "pandas", "pyarrow", "lancedb",
                "graspologic-native", "tiktoken")
    versions = {name: importlib.metadata.version(name) for name in packages}
    if any(versions[name] != config["upstream_version"] for name in packages[:3]):
        raise ValueError("installed Microsoft GraphRAG packages differ from the pinned release")
    return {"commit": config["upstream_commit"], "version": versions["graphrag"],
            "python": sys.version.split()[0], "packages": versions}


def fixture_completion(messages, response_format):
    prompt = messages[-1]["content"]
    if response_format:
        return json.dumps({
            "title": "Registry community", "summary": "Records for a registry community.",
            "findings": [{"summary": "Registry records", "explanation": "See source records."}],
            "rating": 1, "rating_explanation": "Fixture rating.",
        })
    if "-Real Data-" not in prompt:
        return " ".join(item[-1] for item in parse_statements(prompt)) or "Registry entity."
    statements = parse_statements(prompt.rsplit("-Real Data-", 1)[1])
    records = []
    names = {}
    for subject, predicate, _, target, sentence in statements:
        entity_type = {"PRECEDES": "EVENT", "SUBREGION_OF": "GEO"}.get(predicate, "OBJECT")
        names[subject] = names[target] = entity_type
        records.append(f'("relationship"<|>{subject}<|>{target}<|>{sentence}<|>1)')
    entities = [
        f'("entity"<|>{name}<|>{entity_type}<|>Registry entity {name})'
        for name, entity_type in names.items()
    ]
    return "##".join(entities + records + ["<|COMPLETE|>"])


class CallbackState:
    def __init__(self, config):
        self.config = config
        self.models = model_provider(config)
        self.error = None
        self.cache_hits = 0
        self.completions = 0

    async def complete(self, messages, response_format, cache, max_tokens):
        from graphrag_llm.types import LLMChoice, LLMCompletionMessage, LLMCompletionResponse

        if self.error is not None:
            raise RuntimeError("an earlier completion failed") from self.error
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        key = digest({"messages": messages, "format": getattr(response_format, "__name__", None),
                      "max_tokens": max_tokens})
        try:
            text = await cache.get(key) if cache is not None else None
            if text is not None:
                self.cache_hits += 1
            else:
                self.completions += 1
                if self.models is None:
                    text = fixture_completion(messages, response_format)
                else:
                    result = await self.models.chat(
                        messages, response_format={"type": "json_object"} if response_format else None,
                        max_output_tokens=max_tokens,
                    )
                    text = result.choices[0].message.content or ""
                    if result.choices[0].finish_reason == "length":
                        raise ValueError("GraphRAG indexing completion reached its output limit")
            formatted = response_format.model_validate_json(text) if response_format else None
            if cache is not None and not await cache.has(key):
                await cache.set(key, text)
        except Exception as error:
            # Upstream extractors log some callback failures and continue.
            self.error = error
            raise
        return LLMCompletionResponse(
            id=key, created=0, model=self.config["llm_model"], object="chat.completion",
            choices=[LLMChoice(index=0, message=LLMCompletionMessage(
                role="assistant", content=text), finish_reason="stop")],
            formatted_response=formatted,
        )

    async def embed(self, texts):
        from graphrag_llm.types import LLMEmbeddingResponse

        if isinstance(texts, str):
            texts = [texts]
        try:
            if self.models is None:
                vectors = await fixture_embedding(texts, dimension=self.config["embedding_dimension"])
            else:
                vectors = await self.models.embedding(texts)
        except Exception as error:
            self.error = error
            raise
        return LLMEmbeddingResponse(
            model=self.config["embedding_model"], object="list",
            data=[{"object": "embedding", "index": i, "embedding": vector.tolist()}
                  for i, vector in enumerate(vectors)],
            usage={"prompt_tokens": 0, "total_tokens": 0},
        )


def register_callbacks(state):
    from graphrag_llm.completion import register_completion
    from graphrag_llm.embedding import register_embedding

    class Completion:
        def __init__(self, *, tokenizer, cache=None, **kwargs):
            self.tokenizer = tokenizer
            self.cache = cache

        async def completion_async(self, *, messages, response_format=None, **kwargs):
            limit = kwargs.get("max_completion_tokens") or kwargs.get("max_tokens")
            return await state.complete(messages, response_format, self.cache, limit)

    class Embedding:
        def __init__(self, *, tokenizer, **kwargs):
            self.tokenizer = tokenizer

        async def embedding_async(self, *, input, **kwargs):
            return await state.embed(input)

        def embedding(self, *, input, **kwargs):
            return asyncio.run(self.embedding_async(input=input, **kwargs))

    register_completion(MODEL_TYPE, Completion)
    register_embedding(MODEL_TYPE, Embedding)


def native_configuration(request):
    from graphrag.config.embeddings import entity_description_embedding
    from graphrag.config.models.graph_rag_config import GraphRagConfig

    root = Path(request["native_dir"])
    config = request["config"]
    chat_id, embedding_id = "benchmark_chat", "benchmark_embedding"
    chat = {"type": MODEL_TYPE, "model_provider": config["provider"], "model": config["llm_model"]}
    embedding = {"type": MODEL_TYPE, "model_provider": "local", "model": config["embedding_model"]}
    cache_dir = request.get("completion_cache")
    return GraphRagConfig.model_validate({
        "completion_models": {chat_id: chat},
        "embedding_models": {embedding_id: embedding},
        "input_storage": {"base_dir": str(root / "input")},
        "output_storage": {"base_dir": str(root / "tables")},
        "reporting": {"base_dir": str(Path(request["response_file"]).parent / "logs")},
        "cache": {"type": "json", "storage": {"base_dir": cache_dir}} if cache_dir else {"type": "none"},
        "vector_store": {"db_uri": str(root / "lancedb"), "vector_size": config["embedding_dimension"]},
        "concurrent_requests": 1,
        "chunking": {"size": 512, "overlap": 0, "encoding_model": "cl100k_base"},
        "extract_graph": {"completion_model_id": chat_id, "max_gleanings": 0,
                          "entity_types": ["organization", "person", "geo", "event", "object"]},
        "summarize_descriptions": {"completion_model_id": chat_id},
        "community_reports": {"completion_model_id": chat_id, "max_input_length": 2500,
                              "max_length": 450},
        "embed_text": {"embedding_model_id": embedding_id, "names": [entity_description_embedding]},
        "local_search": {"completion_model_id": chat_id, "embedding_model_id": embedding_id,
                         "top_k_entities": config["top_k_entities"], "max_context_tokens": 8000,
                         "top_k_relationships": config["top_k_relationships"]},
    })


def read_tables(root):
    import pandas as pd

    return {name: pd.read_parquet(root / "tables" / f"{name}.parquet") for name in NATIVE_TABLES}


async def index(request, config, state):
    import pandas as pd
    from graphrag.api import build_index

    rows = read_jsonl(request["corpus_file"])
    if not rows or any(row["file_path"] != f'{row["doc_id"]}.txt' for row in rows):
        raise ValueError("Microsoft GraphRAG requires neutral filenames matching corpus IDs")
    documents = pd.DataFrame([
        {"id": row["doc_id"], "title": row["file_path"], "text": row["text"],
         "human_readable_id": i, "raw_data": None}
        for i, row in enumerate(rows)
    ])
    try:
        workflows = await build_index(config, method="standard", input_documents=documents)
    finally:
        if state.models is not None:
            await state.models.client.close()
    if state.error is not None:
        raise RuntimeError("an audited GraphRAG model callback failed") from state.error
    for workflow in workflows:
        if workflow.error is not None:
            raise RuntimeError(f"GraphRAG workflow failed: {workflow.workflow}") from workflow.error
    tables = read_tables(Path(request["native_dir"]))
    docs = tables["documents"]
    if (len(docs) != request["expected_document_count"]
            or dict(zip(docs["id"], docs["title"], strict=True))
            != {row["doc_id"]: row["file_path"] for row in rows}):
        raise ValueError("unverified native document provenance")
    if set(tables["text_units"]["document_id"]) != set(docs["id"]):
        raise ValueError("native text units do not cover the indexed documents")
    return {"status": "complete", "documents_processed": len(docs),
            "table_rows": {name: len(table) for name, table in tables.items()},
            "workflows": [workflow.workflow for workflow in workflows],
            "model_calls": state.completions, "model_cache_hits": state.cache_hits}


def retrieve(request, config):
    from graphrag.config.embeddings import entity_description_embedding
    from graphrag.query.factory import get_local_search_engine
    from graphrag.query.indexer_adapters import (
        read_indexer_entities,
        read_indexer_relationships,
        read_indexer_reports,
        read_indexer_text_units,
    )
    from graphrag.utils.api import get_embedding_store, reformat_context_data

    tables = read_tables(Path(request["native_dir"]))
    level = request["config"]["community_level"]
    communities = tables["communities"]
    engine = get_local_search_engine(
        config=config,
        reports=read_indexer_reports(tables["community_reports"], communities, level),
        text_units=read_indexer_text_units(tables["text_units"]),
        entities=read_indexer_entities(tables["entities"], communities, level),
        relationships=read_indexer_relationships(tables["relationships"]),
        covariates={"claims": []}, response_type="",
        description_embedding_store=get_embedding_store(config.vector_store, entity_description_embedding),
    )
    context = engine.context_builder.build_context(request["query"], **engine.context_builder_params)
    native = reformat_context_data(context.context_records)
    docs = dict(zip(tables["documents"]["id"], tables["documents"]["title"], strict=True))
    units = {str(row.human_readable_id): row for row in tables["text_units"].itertuples(index=False)}
    chunks = []
    for source in native["sources"]:
        unit = units[str(source["id"])]
        if source["text"] != unit.text:
            raise ValueError("native source text differs from its indexed text unit")
        chunks.append({"content": unit.text, "file_path": docs[unit.document_id], "chunk_id": unit.id})
    return {"raw": {
        "status": "success" if chunks or native["entities"] or native["relationships"] else "no_evidence",
        "data": {"chunks": chunks, "entities": [
            {"entity_name": e["entity"], "description": e["description"]} for e in native["entities"]
        ], "relationships": [
            {"src_id": r["source"], "tgt_id": r["target"], "description": r["description"]}
            for r in native["relationships"]
        ]},
        "native_result": native, "native_context": context.context_chunks,
        "native_unavailable": [
            "native_score", "graph_row_source_ids", "retrieved_graph_paths",
            "retrieved_graph_path_length",
        ],
    }}


def main():
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    load_environment()
    request = json.loads(Path(sys.argv[1]).read_bytes())
    native = native_metadata(request["config"])
    operation = request["operation"]
    if operation == "healthcheck":
        from graphrag.api import build_index, local_search

        if not callable(build_index) or not callable(local_search):
            raise RuntimeError("native GraphRAG APIs are unavailable")
        result = {"status": "available"}
    elif operation in ("index", "retrieve"):
        state = CallbackState(request["config"])
        register_callbacks(state)
        config = native_configuration(request)
        if operation == "index":
            result = asyncio.run(index(request, config, state))
        else:
            try:
                result = retrieve(request, config)
            finally:
                if state.models is not None:
                    asyncio.run(state.models.client.close())
        result["usage"] = state.models.usage if state.models is not None else []
    else:
        raise ValueError("unsupported native worker operation")
    write_json(request["response_file"], {**result, "native": native})


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(redact(f"{type(error).__name__}: {error}"), file=sys.stderr)
        sys.exit(1)
