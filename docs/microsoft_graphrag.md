# Microsoft GraphRAG Local Search

The adapter uses Microsoft GraphRAG 3.1.0, commit
`7fc6607edda3d387d23e52ededbf8a75b6730f97`. The worker checks the
installed GraphRAG package versions and records the native runtime and
storage dependencies in each index manifest.
[Pinned upstream release](https://github.com/microsoft/graphrag/releases/tag/v3.1.0)

`graphrag.api.build_index` runs the standard indexing pipeline on one
complete condition corpus. The worker supplies neutral IDs, neutral filenames,
and source text. The native Local Search factory builds retrieval context
from the indexed Parquet tables and LanceDB entity-description vectors.
GraphConflictBench uses its shared final-generation prompt on the packed
evidence, with a 3,072-token limit.

Both profiles use 512-token chunks with no overlap, one extraction pass,
community level 2, up to 40 mapped entities and 40 relationships, and
an 8,000-token native context limit. The worker captures the native context,
including community reports, and passes sources, entities and relationships
through the shared evidence envelope. Source citations use the native
text-unit-to-document mapping and require exact text. Source similarity
scores and graph path lengths are unavailable in the native context.
GraphRAG's default community clustering uses the largest connected
component, and Local Search limits eligible entities by community level.

The indexer clusters the full corpus in each attempt. Failed attempts
retain their logs and tables. On resume, the worker reuses cached completions
for identical requests and rebuilds the native tables. Finished snapshots
are checked by the shared index manifest. Keep the completion cache and
raw traces under the ignored `runs/` directory.

## Windows setup

```powershell
py -3.12 -m venv .venv-microsoft-graphrag
$python = (Resolve-Path '.venv-microsoft-graphrag/Scripts/python.exe').Path
& $python -m pip install -r requirements-locks/microsoft-graphrag-windows.txt
& $python -m pip install --no-deps -e '.[groq]'
$env:TIKTOKEN_CACHE_DIR = (Resolve-Path '.venv/tokenizer-cache').Path
& $python -m graphconflictbench.cli healthcheck --arch microsoft_graphrag

$env:GCB_MICROSOFT_GRAPHRAG_PYTHON = $python
.venv/Scripts/python.exe -m pytest -q tests/integration/test_microsoft_graphrag_native.py
```

Seed the tokenizer cache using the steps in the repository README when
creating a fresh environment. The native fixture test checks two independent
indexes, interrupted-build recovery, reuse, and exact source attribution.

## Groq pilot

The registered callbacks use the repository's guarded Groq GPT-OSS 20B
client and the same local 384-dimensional BGE model as the other
architectures. The live runner uses the frozen pilot, checks the BGE
weights and retains ledger accounting, pacing, and failure captures.

```powershell
& $python scripts/run_groq_pilot.py --arch microsoft_graphrag --key-slot 1 --rotate-on-quota --dry-run
```

The default output root is `runs/microsoft_graphrag-groq-pilot/`. The
live command uses the same arguments without `--dry-run`. A completed
paired run writes its measured breakdown under `results-3072/results_by_hop.json`.
[Saved live pilot report](../results/microsoft_graphrag-groq-pilot-20261125/results_by_hop.json)
