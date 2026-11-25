"""Run HippoRAG 2's native OpenIE, indexing and retrieval in its own environment."""

import asyncio
import importlib.metadata
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

from ..environment import load_environment, redact
from ..generator import NEGATIONS, PHRASES
from ..manifests import digest, read_jsonl, write_json
from ..models import fixture_embedding, parse_statements
from ..providers import model_provider


def native_metadata(config):
    importlib.import_module("pyarrow.parquet")
    dist = importlib.metadata.distribution("hipporag")
    direct = json.loads(dist.read_text("direct_url.json") or "{}")
    actual = {
        "version": dist.version,
        "commit": direct.get("vcs_info", {}).get("commit_id"),
        "url": direct.get("url"),
        "python": sys.version.split()[0],
        "dependencies": {
            name: importlib.metadata.version(name)
            for name in ("igraph", "numpy", "pandas", "pyarrow", "torch")
        },
    }
    if (actual["commit"] != config["upstream_commit"]
            or (actual["url"] or "").removesuffix(".git") != config["upstream_repository"]):
        raise ValueError(f"installed HippoRAG 2 provenance differs from config: {actual}")
    return actual


def fixture_response(prompt):
    marker = "[[ ## fact_before_filter ## ]]"
    if marker in prompt:
        candidates, _ = json.JSONDecoder().raw_decode(prompt.split(marker, 1)[1].lstrip())
        return f"[[ ## fact_after_filter ## ]]\n{json.dumps(candidates)}\n[[ ## completed ## ]]"
    statements = parse_statements(prompt)
    if prompt.startswith("Convert the paragraph"):
        triples = [
            [subject, (PHRASES if positive else NEGATIONS)[predicate], obj]
            for subject, predicate, positive, obj, _ in statements
        ]
        return json.dumps({"triples": triples})
    names = list(dict.fromkeys(name for subject, _, _, obj, _ in statements for name in (subject, obj)))
    return json.dumps({"named_entities": names})


class ModelCallbacks:
    """Bridge synchronous native callbacks to the shared audited provider client."""

    def __init__(self, runner, config, models):
        self.runner = runner
        self.embedding_dim = config["embedding_dimension"]
        self.models = models
        self.failure = None

    def infer(self, messages, *, max_new_tokens, response_format=None):
        if self.failure is not None:
            raise RuntimeError("earlier native model request failed") from self.failure
        if self.models is None:
            return fixture_response(messages[-1]["content"]), {"finish_reason": "stop"}, False
        try:
            response = self.runner.run(self.models.chat(
                messages, response_format=response_format, max_output_tokens=max_new_tokens
            ))
        except Exception as error:
            # Upstream extraction and reranking can catch model errors and continue.
            self.failure = error
            raise
        choice = response.choices[0]
        return choice.message.content or "", {"finish_reason": choice.finish_reason}, False

    def batch_encode(self, texts, **kwargs):
        if self.models is None:
            return self.runner.run(fixture_embedding(list(texts), dimension=self.embedding_dim))
        return self.runner.run(self.models.embedding(list(texts)))


def index(rag, request):
    from hipporag.utils.misc_utils import Chunk

    rows = read_jsonl(request["corpus_file"])
    if not rows or any(row["file_path"] != f'{row["doc_id"]}.txt' for row in rows):
        raise ValueError("HippoRAG 2 requires neutral source filenames matching the corpus IDs")
    prior_texts = rag.chunk_embedding_store.get_all_texts()
    texts = {row["text"] for row in rows}
    if len(texts) != len(rows) or texts & prior_texts:
        raise ValueError("HippoRAG 2 cannot retain distinct sources with identical passage text")
    rag.index([
        Chunk(content=row["text"], source_id=row["doc_id"], metadata={"file_path": row["file_path"]})
        for row in rows
    ])
    store = rag.chunk_embedding_store
    ids = set(store.get_all_ids())
    expected = request.get("expected_document_count", len(rows))
    if len(ids) != expected or not ids <= set(rag.graph.vs["name"]):
        raise RuntimeError(f"native indexing incomplete: passages={len(ids)}, expected={expected}")
    for row in rows:
        metadata = rag.chunk_metadata[store.get_hash_id(row["text"])]
        if metadata["file_path"] != row["file_path"] or metadata["source_id"] != row["doc_id"]:
            raise RuntimeError("native passage attribution differs from the indexed source")
    return {
        "status": "complete",
        "documents_processed": len(ids),
        "graph_vertices": rag.graph.vcount(),
        "graph_edges": rag.graph.ecount(),
    }


def retrieve(rag, query):
    result, = rag.retrieve([query])
    native_result = asdict(result)
    native_result["doc_scores"] = result.doc_scores.tolist()
    chunks = [
        {
            "content": text,
            "file_path": metadata.get("file_path", ""),
            "chunk_id": rag.chunk_embedding_store.get_hash_id(text),
            "native_score": score,
        }
        for text, score, metadata in zip(
            result.docs, native_result["doc_scores"], result.doc_metadata, strict=True
        )
    ]
    return {"raw": {
        "status": "success" if chunks else "no_evidence",
        "data": {"chunks": chunks},
        "native_result": native_result,
        "native_unavailable": ["retrieved_graph_paths", "retrieved_graph_path_length"],
    }}


def execute(request, native, sdk):
    from hipporag.utils.config_utils import BaseConfig

    config = request["config"]
    settings = BaseConfig(
        save_dir=request["native_dir"],
        llm_name=config["llm_model"],
        embedding_model_name=config["embedding_model"],
        openie_max_workers=1,
        retrieval_top_k=config["retrieval_top_k"],
        linking_top_k=config["linking_top_k"],
    )
    with asyncio.Runner() as runner:
        models = model_provider(config)
        callbacks = ModelCallbacks(runner, config, models)
        try:
            with sdk(
                global_config=settings,
                extraction_llm=callbacks,
                embedding_model=callbacks,
                index_identity=digest(config),
            ) as rag:
                if request["operation"] == "index":
                    result = index(rag, request)
                else:
                    result = retrieve(rag, request["query"])
                result = {**result, "native": native, "usage": models.usage if models else []}
                if callbacks.failure is not None:
                    write_json(request["response_file"], result)
                    raise RuntimeError("native model request failed") from callbacks.failure
                return result
        finally:
            if models is not None:
                runner.run(models.client.close())


def main():
    # Keep the dependency's bundled price table even in a networked environment.
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    from hipporag import HippoRAG

    load_environment()
    request = json.loads(Path(sys.argv[1]).read_bytes())
    native = native_metadata(request["config"])
    if request["operation"] == "healthcheck":
        result = {"status": "available", "native": native}
    elif request["operation"] in ("index", "retrieve"):
        result = execute(request, native, HippoRAG)
    else:
        raise ValueError("unsupported native worker operation")
    write_json(request["response_file"], result)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(redact(f"{type(error).__name__}: {error}"), file=sys.stderr)
        sys.exit(1)
