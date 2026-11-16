# GraphConflictBench — Step 4 implementation report

Delivered 15 November 2026. The user's endpoint is the first native LightRAG
integration in the handbook's ordered implementation table.

## Implemented

| Step | Delivered |
| --- | --- |
| 1. Scaffold | Installable Python package, strict Pydantic contracts, versioned configs, CLI, separate core/native dependency locks. |
| 2. Logic | Three typed transitive predicates; explicit negation; time-aware shortest-proof enumeration; all shortest witnesses; source-backed certificates; 12 manually specified logical fixtures. |
| 3. Paired dataset | Deterministic 24-family/48-case pilot; 144 unique source documents; neutral model-visible IDs; source spans and checksums; isolated condition corpora; audit sheet. |
| 4. LightRAG | Official SDK at a pinned commit; two native pilot indexes; hybrid retrieval; raw native traces; conservative quote/source-to-edge mapping; bounded evidence envelope; JSON generation and smoke scoring; immutable snapshots and resumable jobs. |

Upstream LightRAG: `HKUDS/LightRAG`, commit
`f615931d6ab60b179d5347f92a29f75dcff776a6`, installed version 1.5.8 (MIT).
Verified with Python 3.12.14. Runtime and hardware details are in
`docs/environment_report.json`.

## Actual verification

- **43 tests passed**: 42 core tests plus an opt-in native SDK test that built two
  indexes and executed 12 fixture questions. Machine-readable result:
  `results/test-results.xml`.
- All 48 pilot cases passed automatic logical, provenance, text-coverage,
  minimal-depth, pairing, corpus-isolation and integrity checks.
- Both full pilot native indexes processed all **120 documents per condition**.
- **48/48 native pilot retrievals** returned nonempty source contexts with exact
  source-quote mappings; **48/48 generated fixture responses** passed JSON/schema
  validation. The delivered evidence envelopes stayed within 4096 cl100k_base
  tokens.
- Completed dataset/index/run resume verified checksums and reused identical
  results. Source/model/config changes are rejected for stale snapshots.
- Ruff passed; all seven CLI subcommands returned working `--help`; the real-model
  index command's dry-run completed without calling models.

Commands actually executed from the repository root included:

```bash
.venv/bin/python scripts/cache_tokenizers.py
.venv/bin/python -m graphconflictbench.cli validate-ontology
.venv/bin/python -m graphconflictbench.cli generate --size pilot
.venv/bin/python -m graphconflictbench.cli audit --write-report
GCB_NATIVE_PYTHON="$PWD/.venv-lightrag/bin/python" \
  .venv/bin/pytest -q tests --junitxml=results/test-results.xml
.venv/bin/ruff check src tests scripts
.venv/bin/python -m graphconflictbench.cli smoke-adapters \
  --output-dir results/lightrag-pilot
.venv/bin/python -m graphconflictbench.cli smoke-adapters \
  --output-dir results/lightrag-pilot --resume
```

## Limits and remaining work

The native SDK was exercised with deterministic **test extraction, embedding and
answer models**. These are integration checks, not scientific performance
results. Every run is explicitly `benchmark_eligible=false` and
`result_kind=fixture_integration_check`. The logs include unsuccessful proof
retrievals; passing integration does not mean every conflict was correctly found.
No model outputs or research scores were fabricated.

No model credentials were configured and no paid inference requests were made.
The OpenAI-compatible path and provisional model settings are implemented but
have not been verified against a live provider. Human text/label review and a
trained leakage classifier remain pending. Native path IDs and index-level claim
survival are unobservable in this adapter; canonical assertion mapping covers
verbatim source chunks only. Invalid JSON has a separate error denominator; the
small scorer is not the final statistical evaluation suite.

The delivered source reconciles the PDF's 240-case target and handbook's 360-case
alternative as explicit generation settings; only the 48-case pilot is delivered.
The attached handbook's embedded agent prompt was treated as reference text and
did not override the user's explicit Step 4 scope. See `docs/decisions.md`.

HippoRAG 2, PathRAG, Microsoft GraphRAG, oracle ablations, official confidence
intervals, resolution, and a dashboard remain outside this delivery.

## Where to start

Read `README.md`, install the two environments, seed the verified tokenizer cache,
and rerun the fixture smoke in a fresh output directory. The archive contains
source, configs, locks, pilot data, raw native evidence, predictions, scores,
checksums and audit materials. Bundled traces preserve their original execution
paths; rebuild indexes for a different runtime.

The next research step is a **small real-model LightRAG pilot** using reviewed
labels and explicit model/provider/budget settings. Acceptance: both condition
indexes finish, source mappings are audited, raw responses/errors and usage are
retained, and JSON validity/fidelity are measured before expanding the study.
