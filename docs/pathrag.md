# Native PathRAG

GraphConflictBench uses [BUPT-GAMMA/PathRAG](https://github.com/BUPT-GAMMA/PathRAG)
at commit `32567bfc93605b8393996d5fa9ccdc0edbb865b2`. The worker checks the commit,
remote URL and checkout status before importing the native SDK. It indexes
plain source text with `PathRAG.ainsert` and retrieves with
`PathRAG.aquery(..., QueryParam(mode="hybrid", only_need_context=True))`.

The worker supplies explicit LLM and embedding callbacks. A provider import
bridge avoids loading the upstream module's optional backends, including vLLM
on Windows. The checkout's extraction, indexing, path search and storage code
run as shipped. Both profiles use 512-token chunks, no overlap, one extraction
pass and native top-k of 40. The adapter sets the native entity and relationship
stores' cosine cutoff to -1 to keep the ranked candidates. This revision
otherwise switches to a local fallback with an uninitialized source section
when the high-level search yields no candidates.

PathRAG's context string is saved verbatim in the native trace. The adapter
passes returned source text and native graph rows to the shared envelope.
Each index includes a mapping from native document hashes to neutral source paths.
Source attribution requires a text match against that index's native chunk
store. Exact citations still need a quote in both the delivered evidence and
its original document. The context response provides no numeric similarity
scores, directed paths, path lengths or graph-row source IDs.

## Windows setup

The environment uses Python 3.12.1. The lock file pins the SDK's local storage
dependencies and the existing Groq and BGE client stack.

```powershell
git clone https://github.com/BUPT-GAMMA/PathRAG.git .venv-pathrag-src
git -C .venv-pathrag-src checkout --detach 32567bfc93605b8393996d5fa9ccdc0edbb865b2
py -3.12 -m venv .venv-pathrag
$python = (Resolve-Path '.venv-pathrag/Scripts/python.exe').Path
& $python -m pip install -r requirements-locks/pathrag-windows.txt
& $python -m pip install --no-deps -e '.[groq]'
$env:TIKTOKEN_CACHE_DIR = (Resolve-Path '.venv/tokenizer-cache').Path
& $python -m graphconflictbench.cli healthcheck --arch pathrag

$env:GCB_PATHRAG_PYTHON = $python
.venv/Scripts/python.exe -m pytest -q tests/integration/test_pathrag_native.py
```

Seed the tokenizer cache as described in the [repository README](../README.md)
if the cache directory is absent. The fixture test builds independent indexes,
resumes each build from a 15-document checkpoint and reruns scoring on the
same snapshots. Fixture answers have `benchmark_eligible=false`.

## Groq pilot

Use the root `.env` variables and local model cache described in the
[Groq provider guide](groq_provider.md). The runner checks the BGE weights
against the saved LightRAG baseline. It uses Groq GPT-OSS 20B and the same
384-dimensional BGE embedding model, frozen pilot cases, shared final prompt
and 3,072-token evidence budget. It keeps the existing capture and spending
ledger, 10-document checkpoint batches and 30-second indexing and 60-second
scoring intervals. The pilot remains provisional.

```powershell
& $python scripts/run_groq_pilot.py --arch pathrag --key-slot 1 --rotate-on-quota --dry-run
& $python scripts/run_groq_pilot.py --arch pathrag --key-slot 1 --rotate-on-quota
```

The optional rotation waits for the captured HTTP 429 Retry-After interval,
uses the existing ledger recovery checks and attempts the next configured key.
It wraps to the first key after the last. The same command can resume the
local pilot after an interruption. Results, checkpoints and raw case traces
are under `runs/pathrag-groq-pilot/`.
