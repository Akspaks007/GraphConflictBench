# Saved Groq pilot indexes

`groq-pilot/conflict` and `groq-pilot/control` contain the original native
LightRAG stores for the completed 120-document indexes. Each snapshot includes
its indexed corpus and a manifest with file checksums, build provenance and the
required local embedding model revision. The snapshots can be committed as
regular Git files. The live 3,072-token evaluation breakdown is in
[`groq-pilot/results_by_hop.json`](groq-pilot/results_by_hop.json).

## Reuse the indexes

From the repository root, use the matching code, Python 3.12.13, the pinned
LightRAG SDK and the local BGE model specified in the manifests. The
[Groq setup guide](../docs/groq_provider.md) explains how to prepare the native
environment and model cache.

```powershell
$python = (Resolve-Path '.venv-lightrag/Scripts/python.exe').Path
& $python scripts/restore_indexed_graphs.py --worker-python $python
```

The restore command verifies both snapshots and prepares local index
directories under `indexes/groq-saved/` without calling Groq. Use
`indexes/groq-saved/conflict` or `indexes/groq-saved/control` as the
`--index-dir` for the matching condition in the `run` command. Live retrieval
and answer generation use your configured provider and spending ledger.
