# HippoRAG 2 integration

The `hipporag2` architecture uses the official [OSU-NLP-Group/HippoRAG SDK](https://github.com/OSU-NLP-Group/HippoRAG/tree/d5c8329422e0a0b834a15874545cb6a74b4f9b26),
version `2.0.0a5` at commit `d5c8329422e0a0b834a15874545cb6a74b4f9b26` (MIT).
The worker checks its installed VCS provenance and Parquet support. The
[Windows lock](../requirements-locks/hipporag2-windows.txt) pins its dependencies.

## Run the offline fixture

From the repository root on Windows with Python 3.12, after setting up the core
environment described in the [README](../README.md):

```powershell
& ./.venv/Scripts/python.exe -m venv .venv-hipporag
& ./.venv-hipporag/Scripts/python.exe -m pip install -r requirements-locks/hipporag2-windows.txt -e '.[groq]'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'
& ./.venv/Scripts/python.exe scripts/cache_tokenizers.py
& ./.venv/Scripts/python.exe -m graphconflictbench.cli healthcheck --arch hipporag2
& ./.venv/Scripts/python.exe -m graphconflictbench.cli smoke-adapters --arch hipporag2 --output-dir runs/hipporag2-fixture-local

$env:GCB_HIPPORAG2_PYTHON = (Resolve-Path '.venv-hipporag/Scripts/python.exe').Path
& ./.venv/Scripts/pytest.exe -q tests/integration/test_hipporag2_native.py
```

Use a fresh output directory after changes to settings or implementation.
Use `--resume` for a checksum-matching completed index or run. The CLI also
supports `index` and `run` per condition, and `index --batch-size N` for
checkpointed indexing. `--worker-python` selects a different installed worker.

## Source attribution and traces

- The native `index()` call receives unmodified source text and a neutral
  source ID and filename through the SDK's `Chunk` input. The SDK preprocessor
  retains one passage per document. The adapter rejects identical passage text
  with distinct source IDs because the SDK deduplicates passages by text and
  would otherwise lose source attribution.
- The native `retrieve()` call can use OpenIE facts, recognition memory and
  personalized PageRank to return ranked passages. Each native JSON trace
  contains the returned passages, scores, source metadata and graph seeds. The
  trace records retrieved graph paths and path length as unavailable.
- The final prompt receives attributed verbatim passages within 3,072
  `cl100k_base` tokens. Source attribution uses SDK passage metadata followed
  by the shared exact-quote check. Native graph seeds are retained in the
  audit trace. Fixture runs carry `benchmark_eligible=false`.

[Recorded fixture verification and per-hop results](../results/hipporag2-fixture-20261124/verification.json)

## Groq configuration

[The Groq profile](../configs/architectures/hipporag2-groq.yaml) uses the shared
audited Groq transport and policy, `openai/gpt-oss-20b`, and local 384-dimensional
BGE vectors. The same embedding cache and ledger setup in the [Groq guide](groq_provider.md)
apply. Native NER, triple extraction and recognition-memory calls go through the
guard with their native output limits, bounded by the frozen policy.

The local cache uses the Qdrant snapshot at revision
`aa8f8b060edb00e03bfdd08813a2949946c8ba55`. The five files retrieved from
ModelScope matched the archived LightRAG checksums and produced a
384-dimensional embedding offline. [ModelScope copy](https://www.modelscope.cn/models/Qdrant/bge-small-en-v1.5-onnx-Q) · [LightRAG snapshot manifest](../indexed_graphs/groq-pilot/conflict/snapshot_manifest.json)

Use the HippoRAG environment to inspect the checkpointed plan for the frozen
48-case pilot. `--key-slot 1` selects the first configured credential for the
entire run. The shared ledger paces that credential across workers.

```powershell
& ./.venv-hipporag/Scripts/python.exe scripts/run_groq_pilot.py --arch hipporag2 --key-slot 1 --dry-run
```

An authorized live run uses the same command without `--dry-run`. The runner
verifies the BGE cache revision and checksums against the archived LightRAG
manifest before any dispatch. It builds each condition in 10-document
checkpoints, uses 30-second indexing and 60-second scoring intervals per key,
and writes the 3,072-token results under
`runs/hipporag2-groq-pilot/results-3072/` by default. Use a fresh
`--output-root` when settings change and the same root for a matching resume.

The runner writes `results_by_hop.json` after both runs complete. The standalone
reporter can also verify and summarize any saved complete pair for the frozen
pilot, including a fixture pair:

```powershell
& ./.venv/Scripts/python.exe scripts/report_pilot_by_hop.py runs/hipporag2-fixture-recheck-20261124/results
```

Each row records eight cases for a hop and condition. `tp` and `fn` are
detected and missed conflicts, `fp` and `tn` are false alarms and correctly
cleared controls, and `error` counts invalid answers. Complete-proof retrieval
uses delivered source text and is measured independently of answer validity.
`exact_proofs` counts complete citations with correct supporting and opposing
roles. Controls have no gold conflict proof, so their retrieval field is null.
