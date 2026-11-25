"""Call the pinned PathRAG indexing and hybrid retrieval APIs."""

import asyncio
import csv
import importlib.metadata
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

from ..environment import load_environment, redact
from ..generator import NEGATIONS, PHRASES
from ..manifests import read_jsonl, write_json
from ..models import fixture_embedding, parse_statements
from ..providers import model_provider


def unavailable_upstream_provider(*args, **kwargs):
    raise RuntimeError("PathRAG must use the benchmark model callbacks")


def load_native(config):
    root = Path(os.environ.get(
        "GCB_PATHRAG_SOURCE", Path(__file__).resolve().parents[3] / ".venv-pathrag-src"
    )).resolve()
    git = ["git", "-c", f"safe.directory={root.as_posix()}", "-C", str(root)]
    commit = subprocess.check_output([*git, "rev-parse", "HEAD"], text=True).strip()
    url = subprocess.check_output([*git, "remote", "get-url", "origin"], text=True).strip()
    if commit != config["upstream_commit"] or url.removesuffix(".git") != config["upstream_repository"]:
        raise ValueError("PathRAG checkout provenance differs from config")
    if subprocess.check_output([*git, "status", "--porcelain", "--", "PathRAG"], text=True).strip():
        raise ValueError("PathRAG checkout contains changes to native code")
    # The upstream provider module eagerly imports vLLM and other unused backends.
    providers = ModuleType("PathRAG.llm")
    providers.openai_complete = unavailable_upstream_provider
    providers.openai_embedding = unavailable_upstream_provider
    sys.modules["PathRAG.llm"] = providers
    sys.path.insert(0, str(root))
    sdk = importlib.import_module("PathRAG")
    if Path(sdk.__file__).resolve().parent != root / "PathRAG":
        raise ValueError("loaded PathRAG from an unexpected location")
    return sdk, {
        "commit": commit, "url": url, "python": sys.version.split()[0],
        "dependencies": {
            name: importlib.metadata.version(name)
            for name in ("nano-vectordb", "networkx", "numpy", "tiktoken", "tqdm")
        },
        "provider_bridge": "explicit-callbacks-v1",
    }


def fixture_response(prompt, keyword_extraction):
    input_text = prompt.rsplit("-Real Data-", 1)[-1]
    if keyword_extraction:
        return json.dumps({
            "high_level_keywords": ["registry relationship"],
            "low_level_keywords": re.findall(r"N[0-9a-f]{20}", input_text) or [input_text.strip()],
        })
    records = []
    names = {}
    for subject, predicate, positive, obj, sentence in parse_statements(input_text):
        names[subject] = names[obj] = predicate
        label = (PHRASES if positive else NEGATIONS)[predicate]
        records.append(
            f'("relationship"<|>{subject}<|>{obj}<|>{sentence}<|>{label}<|>1)'
        )
    entities = [
        f'("entity"<|>{name}<|>{category}<|>Registry entity {name})'
        for name, category in names.items()
    ]
    return "##".join(entities + records + ["<|COMPLETE|>"])


async def index(rag, request):
    from PathRAG.utils import compute_mdhash_id

    rows = read_jsonl(request["corpus_file"])
    if not rows or any(row["file_path"] != f'{row["doc_id"]}.txt' for row in rows):
        raise ValueError("PathRAG requires neutral filenames matching corpus IDs")
    mapping_file = Path(request["native_dir"]) / "benchmark_sources.json"
    mapping = json.loads(mapping_file.read_bytes()) if mapping_file.is_file() else {}
    batch = {
        compute_mdhash_id(row["text"].strip(), prefix="doc-"): row["file_path"] for row in rows
    }
    if len(batch) != len(rows) or batch.keys() & mapping.keys():
        raise ValueError("PathRAG cannot attribute distinct sources with identical document text")
    await rag.ainsert([row["text"] for row in rows])
    mapping.update(batch)
    expected = request.get("expected_document_count", len(rows))
    native_docs = set(await rag.full_docs.all_keys())
    native_chunks = await rag.text_chunks.get_by_ids(await rag.text_chunks.all_keys())
    if (len(mapping) != expected or native_docs != mapping.keys()
            or {chunk["full_doc_id"] for chunk in native_chunks} != native_docs):
        raise RuntimeError(f"native indexing incomplete: documents={len(native_docs)}, expected={expected}")
    write_json(mapping_file, mapping)
    graph = rag.chunk_entity_relation_graph
    return {
        "status": "complete", "documents_processed": len(native_docs),
        "graph_vertices": graph._graph.number_of_nodes(),
        "graph_edges": graph._graph.number_of_edges(),
    }


def context_section(result, heading):
    if not result:
        return ""
    marker = re.escape(f"-----{heading}-----")
    match = re.search(rf"(?ms)^{marker}\n```csv\n(.*?)\n```$", result)
    return match[1] if match else ""


def graph_rows(result, section_suffix, fields):
    rows = []
    for level in ("high", "low"):
        section = context_section(result, f"{level}-level {section_suffix} information")
        for row in csv.DictReader(io.StringIO(section)):
            item = {field: row[column] for column, field in fields.items() if row.get(column)}
            if item and item not in rows:
                rows.append(item)
    return rows


async def retrieve(rag, query_param, request):
    result = await rag.aquery(request["query"], param=query_param)
    root = Path(request["native_dir"])
    paths = json.loads((root / "benchmark_sources.json").read_bytes())
    ids = await rag.text_chunks.all_keys()
    stored = await rag.text_chunks.get_by_ids(ids)
    by_text = {
        chunk["content"]: (chunk_id, paths[chunk["full_doc_id"]])
        for chunk_id, chunk in zip(ids, stored, strict=True)
    }
    chunks = []
    # Native context removes CSV quoting when it combines the source sections.
    sources = context_section(result, "Sources")
    for text in re.findall(r"(?ms)^\d+,\t(.*?)(?=\n\d+,\t|\Z)", sources):
        chunk_id, path = by_text.get(text, (None, ""))
        chunks.append({"content": text, "file_path": path, "chunk_id": chunk_id})
    entities = graph_rows(result, "entity", {
        "entity": "entity_name", "type": "entity_type", "description": "description",
    })
    relationships = graph_rows(result, "relationship", {
        "source": "src_id", "target": "tgt_id", "description": "description", "keywords": "keywords",
    })
    return {"raw": {
        "status": "success" if chunks or entities or relationships else "no_evidence",
        "data": {"chunks": chunks, "entities": entities, "relationships": relationships},
        "native_result": result,
        "native_unavailable": [
            "native_score", "graph_row_source_ids", "retrieved_graph_paths",
            "retrieved_graph_path_length",
        ],
    }}


async def execute(request, sdk):
    from PathRAG.utils import EmbeddingFunc

    config = request["config"]
    models = model_provider(config)
    dimension = config["embedding_dimension"]

    async def llm(prompt, **kwargs):
        if models is None:
            return fixture_response(prompt, kwargs.get("keyword_extraction", False))
        return await models.llm(prompt, **kwargs)

    async def embedding(texts):
        if models is None:
            return await fixture_embedding(texts, dimension=dimension)
        return await models.embedding(texts)

    try:
        rag = sdk.PathRAG(
            working_dir=request["native_dir"],
            llm_model_name=config["llm_model"], llm_model_func=llm, llm_model_max_async=1,
            embedding_func=EmbeddingFunc(embedding_dim=dimension, max_token_size=512, func=embedding),
            chunk_token_size=512, chunk_overlap_token_size=0, entity_extract_max_gleaning=0,
        )
        # This revision does not forward vector_db_storage_cls_kwargs to its stores.
        for store in (rag.entities_vdb, rag.relationships_vdb):
            store.cosine_better_than_threshold = config["cosine_threshold"]
        if request["operation"] == "index":
            result = await index(rag, request)
        else:
            param = sdk.QueryParam(
                mode="hybrid", only_need_context=True, top_k=config["retrieval_top_k"]
            )
            result = await retrieve(rag, param, request)
        return {**result, "usage": models.usage if models else []}
    finally:
        if models is not None:
            await models.client.close()


def main():
    load_environment()
    request = json.loads(Path(sys.argv[1]).read_bytes())
    sdk, native = load_native(request["config"])
    if request["operation"] == "healthcheck":
        result = {"status": "available"}
    elif request["operation"] in ("index", "retrieve"):
        result = asyncio.run(execute(request, sdk))
    else:
        raise ValueError("unsupported native worker operation")
    write_json(request["response_file"], {**result, "native": native})


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(redact(f"{type(error).__name__}: {error}"), file=sys.stderr)
        sys.exit(1)
