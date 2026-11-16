# Gemini integration report - Step 4, optional provider

Recorded 15 November 2026, Asia/Calcutta. Implementation and offline verification are complete. **No live Gemini requests were made, no billing settings were changed, and no additional GraphRAG architecture was started.** Live evaluation remains blocked on the project/model and human-review checks below.

The prepared configuration is [proposed-plan-v3/lightrag-gemini.yaml](proposed-plan-v3/lightrag-gemini.yaml). Its eligibility status is deliberately **unverified**; its live ledger has not been initialized. Earlier proposal directories are retained drafts. Exact Windows instructions are in [POWERSHELL_COMMANDS.md](POWERSHELL_COMMANDS.md); they distinguish offline setup, one subsequently approved connectivity request, and a separately approved staged evaluation.

## Changes and preserved behavior

| Area | Implementation |
| --- | --- |
| Provider selection | New `providers.py` factory selects fixture, existing OpenAIModels, or optional GeminiModels. Final inference and native worker use this factory. |
| Gemini transport | New `gemini_models.py` implements explicit REST `generateContent` and `embedContent` callbacks through httpx. No SDK discovery, countTokens, files, tools, grounding, redirects or automatic retries. |
| Gemini controls | New `gemini_control.py` supplies a separate frozen Gemini policy, project attestation gate, atomic quota reservations and Gemini-specific paid-equivalent accounting. It reuses generic ledger/capture operations, not OpenAI prices. |
| Configuration | New `configs/architectures/lightrag-gemini.yaml`; strict provider/model/dimension/task checks; concurrency 1 and retries 0. The bare template cannot call a provider without a frozen policy. |
| CLI | New offline `gemini-control init/status/verify` and single-request `gemini-check`. Existing OpenAI commands are preserved. |
| Dotenv and redaction | New `environment.py` loads the explicit repository-root `.env` before CLI/worker dispatch and installs credential-safe diagnostics. Blank `.env.example` documents both providers. |
| Dependencies | `python-dotenv>=1.2,<2` is a base dependency; core lock now pins 1.2.4. The native lock already pinned 1.2.4. Optional `gemini` extra declares httpx and NumPy. |
| Offline preparation | `scripts/prepare_gemini_plan.py` writes fresh, hashed plans without network access; `scripts/verify_gemini_offline.py` checks lineage, prompt leakage, audits and test reports. |

The pinned official LightRAG 1.5.8 / commit `f615931d6ab60b179d5347f92a29f75dcff776a6` still performs extraction, native indexing and hybrid retrieval. The worker's normal subprocess boundary remains; only the Gemini HTTP-mock SDK test runs its same worker function in-process to intercept transport. Existing fixture integration separately exercises the real subprocess.

No source changes were made to the OpenAI wrapper (`models.py`) or its spending/capture implementation (`provider_control.py`). The ontology, canonical datasets, proof verifier, evidence mapping, v2 metadata allowlist, role-aware and legacy metrics, shared generation prompt, and runner are byte-identical to the before-task archive. Wiring/configuration changes are included in implementation hashes, preventing old snapshot reuse.

The shared 4,096-token evidence envelope, source/entity/relationship ordering and native retrieval allowances remain unchanged. The previous relationship-row budget issue is not resolved by this provider addition and must still be considered when interpreting retrieval. Paired conditions retain separate indexes. Canonical graphs, labels and proof sets never enter native ingestion or final generation. Fixture/mock results remain `benchmark_eligible=false`; the proposed Gemini smoke configuration also remains ineligible pending review.

## Model availability, dimensions and eligibility

Public documentation was checked on 15 November 2026. **Gemini 2.5 Flash is deprecated and API access is limited to existing users. From December 1, 2026, Google says requests to its old name will route to Gemini 3.5 Flash-Lite at that model's rates.** A newly created key does not establish access. This implementation blocks dispatch on/after December 1 UTC and rejects a returned model version outside the approved 2.5 Flash family. It never silently selects a replacement. [Google model notice](https://aistudio.google.com/docs/models/gemini-2.5-flash).

`gemini-embedding-001` remains documented for text input, with a 2,048-token input limit and recommended dimensions 768, 1,536 or 3,072. The proposal explicitly uses **1,536 dimensions**. [Embedding model specification](https://aistudio.google.com/docs/models/gemini-embedding-001). Google requires manual normalization of its reduced-dimension vectors; the callback applies L2 normalization after validating shape, finite values and nonzero norm. Raw response vectors are captured before normalization. [Normalization guidance](https://aistudio.google.com/docs/embeddings#quality-for-smaller-dimensions).

Indexing and retrieval use the same model, dimension, normalization and symmetric `SEMANTIC_SIMILARITY` task. These are frozen in the adapter and policy and checked before use. This task is an explicit proposal, not a claim of optimal retrieval quality. Gemini's 2,048-token embedding maximum is passed to native LightRAG. A stricter UTF-8 byte-based bound rejects possibly oversized requests without truncating source material; it can reject a text that Google's tokenizer would accept. OpenAI vectors are never reused even when their dimension matches.

Google publishes free-tier entries for these models, but **this project's eligibility and active quotas have not been verified**. The code does not infer free service from a key or request account/billing data. [Published pricing](https://aistudio.google.com/docs/pricing). Human confirmation of model access, tier, project reference, review date and active quotas is required before initialization. Attestations expire after seven days or the earlier model-routing deadline.

## Secret handling

`load_dotenv()` uses `override=False`, `interpolate=False` and an explicit repository-root path. Externally supplied variables take precedence. The native subprocess inherits the parent environment and also loads the same root file; its temporary CWD is not searched. Gemini authentication uses only `GEMINI_API_KEY`, sent in `x-goog-api-key`, never in the URL or CLI arguments.

The existing private `.env` was not rewritten, displayed, copied, hashed or archived. The user's existing `.gitignore` rules already excluded `.env` and `.env.*` while allowing `.env.example`; those bytes were preserved. The public example contains empty assignments only. Runtime dotenv loading reads credentials into process memory as requested; no credential value or fingerprint enters a report or manifest.

Authentication headers are excluded from capture. Known credentials, including URL/JSON-escaped variants, are redacted from logs, exceptions and response bodies before writing. A credential echo causes a redacted capture and freezes the ledger. Offline tests cover external-variable precedence, CLI ordering, inherited worker environment, Git ignore behavior and redacted transport/CLI/log failures. Final artifact scanning found no configured credential in public output. This checks known configured secrets, not every possible unknown secret encoding.

## Quotas, usage, capture and the $2 ceiling

Defaults are **500 requests total**, **200 per rolling 24 hours**, **at least 31 seconds between dispatches**, **40,000 conservative input-bound units per minute**, concurrency 1 and retries 0. Operators must lower these to their actual project limits. Google applies quotas per project rather than per key, with daily resets at midnight Pacific; the local combined rolling-day guard is intentionally more restrictive. Other applications on the project can still exhaust provider quota. [Google quota documentation](https://aistudio.google.com/docs/rate-limits).

One persistent SQLite ledger covers connectivity, extraction/gleaning/summaries, indexing embeddings, retrieval keyword generation/query embeddings and final generation, across both conditions. Atomic reservations occur before dispatch. A 429 preserves its body and Retry-After information, freezes further traffic and never retries or changes tier. Lifetime/day counts are not refunded after errors. Unknown failures retain their full spending reservation.

The policy reserves at standard Gemini-specific rates: **$0.30/M input tokens, $2.50/M output tokens and $0.15/M embedding input tokens**, even for a human-confirmed free-tier project. Thinking is disabled, outputs capped at 1,536, and tools/multimodal/unpriced request options are rejected. [Google pricing](https://aistudio.google.com/docs/pricing#gemini-2.5-flash). Missing or inconsistent generation usage freezes the ledger; absent embedding usage consumes its conservative upper bound and is explicitly logged as unknown, never zero/free.

The **$2 paid-equivalent reservation ceiling is application protection, not an unconditional account invoice cap**. It depends on current prices, conservative token bounds and truthful usage; it excludes external project traffic, taxes, billing anomalies and manual ledger changes. No provider-side account spending limit was configured or verified. Eligibility, accounting basis and uncertainty remain explicit in status/usage records. Do not reset a ledger, silently raise limits or enable billing after a failure.

For scale only, an illustrative workload of 0.36M generation input tokens, 0.04M output tokens and 0.05M embedding input tokens costs about **$0.22 at these paid-equivalent rates**. This is a planning scenario, not measured Gemini usage or a guarantee. Real extraction length, summaries, failures and absent embedding usage can increase reservations or stop a stage before the ceiling.

The previous 1,800-second worker timeout would interrupt a slow Gemini index. Gemini index/query operations now receive `1800 + min(total request cap, rolling-day cap) * (minimum spacing + 180)` seconds of subprocess headroom, derived from the frozen policy. This changes no request/token/spend allowance or retrieval budget. OpenAI, fixture and metadata healthchecks retain 1,800 seconds. A regression test covers this boundary.

The offline native mock workload produced **420 simulated HTTP callbacks**: 144 generation and 276 embeddings, about 180 callbacks per condition index and 30 per six-case run. These are plumbing observations with fixture responses, not forecasts of real provider usage. A later connectivity test adds one request. At 31 seconds between dispatches, 420 callbacks alone imply over 3.6 hours, plus processing and rolling-day waits. The default 200/day cap requires multiple days. If actual project quotas cannot accommodate a complete index operation, the unchanged protocol is blocked; dropping documents, gleaning or cases to fit is not authorized.

Captures preserve request JSON, non-secret headers, decompressed raw/partial/error response bodies, quota errors, usage/model versions and checksums. Only credential occurrences are redacted. Files use create-once semantics and hashes; they are not hardware WORM storage. Fresh index/run/plan paths are required after any source, model, prompt or policy change. An initial offline native callback-copy failure is retained under `gemini-native-first`; Gemini's callback owner now shares its guarded client when native dataclass copying occurs, avoiding an uncopyable HTTP lock.

## Offline validation

Authoritative evidence for the final source: [verification-release.json](verification-release.json), [unit-release.xml](unit-release.xml), [integration-release.xml](integration-release.xml), [ruff-release.txt](ruff-release.txt). Earlier `verified`/`complete` reports are retained evidence from before the Gemini timeout adjustment.

[GEMINI_MANIFEST_FINAL.json](GEMINI_MANIFEST_FINAL.json) records public delivery/source checksums and changed/new source paths against the archived before-task code and existing v2 manifest. The first manifest is retained as an intermediate snapshot; the final inventory distinguishes the pre-existing original artifact manifest from new source files. Private dotenv files, caches and pytest junction aliases are excluded. Package versions and dependency consistency are recorded in [environment-release.json](environment-release.json).

| Check | Result |
| --- | --- |
| Core unit suite | 94 passed; zero failures/errors/skips |
| Full integration suite, native opt-in enabled | 24 passed; zero failures/errors/skips |
| Total | **118 passed** |
| Ruff over `src tests scripts` | Passed |
| Dependency consistency | `pip check` passed in both Windows environments |
| Original 48-case pilot audit | Passed: 24 families, 144 documents, valid certificates and paired queries |
| V2 stratified 12-case audit | Passed: six families, 36 unique documents, all three predicates and depths; 30 documents per condition |
| Historical data/result hashes | **2,219 files unchanged** against the v2 manifest |
| V2 prompt replay | All 48 prompts match prior v2 text/hashes and pass metadata/gold-field leakage checks |
| Fresh native final prompts | 24 checked across fixture and mocked-Gemini integrations |
| Gemini REST final-generation payloads | All 12 use the exact fixed shared system prompt and filtered evidence |
| Prepared live plan | Unverified, no initialized ledger, no live indexes/runs |

The Gemini-native test runs actual pinned LightRAG extraction/indexing/hybrid retrieval on the v2 stratified dataset with mocked HTTP responses and a fake quota clock. It covers both isolated indexes and all 12 final generations. Separate HTTP tests cover usage, normalized vectors, quota failures, partial/network/HTTP failures, model substitutions, credential echoes and exactly-one-request connectivity semantics. Existing OpenAI transport and native fixture tests also pass. None establish real-model extraction quality, access or free eligibility. Python reports 3.12.10 in the current verified native environment; this is the observed runtime rather than an assumption from older environment notes.

To repeat tests without overwriting this evidence, choose a new `$check` directory:

```powershell
$native = (Resolve-Path .venv-lightrag/Scripts/python.exe).Path
$check = 'results/gemini-integration-rerun-v1'
$env:GCB_NATIVE_PYTHON = $native
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'
& .venv/Scripts/python.exe -B -m pytest -q tests/unit --junitxml "$check/unit.xml"
& $native -B -m pytest -q tests/integration --basetemp "$check/integration" --junitxml "$check/integration.xml"
& .venv/Scripts/python.exe -B -m ruff check src tests scripts
& .venv/Scripts/python.exe -B -m pip check
& $native -B -m pip check
& $native -B -m graphconflictbench.cli audit --dataset data/generated/pilot
& $native -B -m graphconflictbench.cli audit --dataset results/step4-validity-v2-20261115/stratified-smoke-v2
```

`verify_gemini_offline.py` verifies this delivered evidence layout and refuses to overwrite `verification-release.json`. A rerun needs a fresh evidence root with the same input layout or a separately versioned verification script; do not overwrite this report's fixtures to reuse its command.

## Remaining gates and proposed evaluation

1. **Model access:** establish existing-user access to 2.5 Flash before the December 1 deadline. If unavailable, explicitly review a new model/configuration/pricing/protocol; no automatic migration is implemented.
2. **Eligibility and quota feasibility:** inspect the intended project's actual tier and both models' active quotas. Record a non-secret reference, lower local limits as necessary, and confirm a full index can finish. No project attestation has been supplied here.
3. **Human benchmark review:** complete the existing [stratified 12-case worksheet](../step4-validity-v2-20261115/final-plan/human_review_smoke12.html), including negation, source provenance, proof paths and ambiguities. Automated certificates do not complete this review; no leakage classifier has been trained.
4. **Separate live approval:** execute the single connectivity command only after approval; inspect its capture/ledger. Embedding correctness and extraction fidelity remain untested against Google until the separately approved staged evaluation.
5. **Stage review:** reuse exactly `results/step4-validity-v2-20261115/stratified-smoke-v2`, six cases per condition with all three predicates/depths. Build a fresh conflict index, inspect extraction evidence, run its six cases, then repeat for control as quota permits. Preserve the one shared ledger and every failure. No `--limit` slice, gold-label change or alternate architecture is proposed.

The subsequent approved index/run roots are `indexes/gemini/stratified-v1-20261115/{condition}` and `runs/gemini/stratified-v1-20261115/{condition}`. The exact commands, one-request connectivity path, approval distinction and capture locations are in [POWERSHELL_COMMANDS.md](POWERSHELL_COMMANDS.md). All of these live paths remain uncreated.
