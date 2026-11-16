# Gemini commands — prepared only, not executed against Google

Run from the GraphConflictBench repository root. All generation/embedding traffic below remains subject to separate live-test approval. Do not enable billing. No command below prints a credential or needs it as an argument.

## Local key and offline checks

Keep the existing repository-root `.env` in your editor with a `GEMINI_API_KEY=` assignment containing your own local value. Do not overwrite an existing `.env` with `.env.example`. The CLI calls `load_dotenv(..., override=False)` before provider initialization. Explicit shell variables take precedence, and the native worker inherits them and loads the same root file without overriding them. No `GOOGLE_API_KEY` fallback is used. `.env` and `.env.*` are ignored; `.env.example` is allowed and has no credential.

```powershell
$python = (Resolve-Path .venv-lightrag/Scripts/python.exe).Path
$root = 'results/gemini-integration-v1-20261115'
$dataset = 'results/step4-validity-v2-20261115/stratified-smoke-v2'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'

# Offline only: SDK metadata and dataset checks; not Google API connectivity.
& $python -B -m graphconflictbench.cli healthcheck --config "$root/proposed-plan-v3/lightrag-gemini.yaml" --worker-python $python
& $python -B -m graphconflictbench.cli audit --dataset $dataset
```

The prepared proposal is intentionally unverified and cannot send an API request. Public docs list free-tier pricing but do not establish your project's model access or billing eligibility. Gemini 2.5 Flash access is restricted to existing users; it automatically reroutes December 1, 2026. This integration stops before that date and rejects another model in the response. If your project cannot use the requested model, stop and review a replacement explicitly.

## Prepare a fresh attested plan only after human checks

Confirm the key belongs to the intended project, that the requested models are accessible, its free-tier status, and its current per-model RPM/TPM/RPD limits in AI Studio. Do not select `free-tier-confirmed` without this evidence. A new key does not establish any of it. The following is the **free-tier-confirmed** example, not a claim about your account. It neither enables nor changes billing.

```powershell
$reference = Read-Host 'Confirmed project ID and model/tier/quota review reference (NOT the API key)'
$daily = [int](Read-Host 'Conservative combined rolling-24h request cap, <=200 and within confirmed project limits')
$spacing = [int](Read-Host 'Seconds between requests, >=31; use >=61 for a 1-RPM project limit')
$tpm = [int](Read-Host 'Conservative combined input bound per minute, <=40000 and within confirmed limits')
$checkedUtc = [DateTime]::UtcNow.ToString('yyyy-MM-dd')

& $python -B scripts/prepare_gemini_plan.py --output "$root/approved-plan-v1" --eligibility-status free-tier-confirmed --eligibility-reference $reference --eligibility-checked-on $checkedUtc --quotas-reviewed --max-requests 500 --max-requests-per-24h $daily --min-interval-seconds $spacing --max-input-tokens-per-minute $tpm
if ($LASTEXITCODE -ne 0) { throw 'Plan preparation failed; no API call was made.' }

$plan = "$root/approved-plan-v1"
$config = "$plan/lightrag-gemini.yaml"
$policy = "$plan/gemini-policy.json"

# Offline initialization: one ledger for connectivity, both indexes and all queries.
& $python -B -m graphconflictbench.cli gemini-control init --policy $policy
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy
```

Every output/plan path must be new. Never edit a frozen policy in place or delete/reinitialize its ledger to obtain another allowance. The schema caps total requests at 500, rolling-24h requests at 200, dispatch rate below two per minute and input reservations at 40,000 per minute. Choose lower limits when required by your actual project. These local limits combine both models and may be stricter than Google's independent quotas. Google resets daily quotas at midnight Pacific time; this guard deliberately uses a rolling 24 hours instead.

The code reserves at Gemini-specific paid-equivalent prices even when a human confirms free-tier eligibility. It does not prove requests will be free or query account billing. For an already-paid project, a separate explicit authorization and a `paid-tier-confirmed` declaration would be required; do not use it to bypass the current no-billing instruction.

## One connectivity request — only after approval

```powershell
& $python -B -m graphconflictbench.cli gemini-check --config $config --output-dir "$root/connectivity-v1"
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy
```

`gemini-check` makes exactly **one `generateContent` request** asking for `OK`. It makes no discovery, countTokens, embedding or billing calls and has no automatic retry. It saves `connectivity.json` or a credential-safe `error.json` in a fresh directory; full redacted HTTP evidence goes into the shared ledger capture. It verifies generation connectivity/model version, not live embedding behavior. Do not rerun into the same path or blindly repeat a failed request. A 403/404 may indicate project/model ineligibility; a 429 freezes further traffic without upgrading the tier.

## Staged twelve-case native LightRAG evaluation — separate later approval

Before each operation, inspect `gemini-control status` for remaining money, total requests and rolling-24h usage, plus the project's actual quotas. The offline mock workload used about **180 HTTP requests per condition index** and **30 per condition run** (420 total, plus connectivity); real extraction can require more. A project with fewer than the required per-operation generation/embedding quotas cannot complete this protocol unchanged. Do not start an index that is known to exceed the available allowance. Do not remove gleaning, drop cases, change proof depth, truncate documents or enable billing to fit quotas without a separate reviewed decision.

With the default local 200-request rolling-day cap, the entire study cannot finish in one day. Leave sufficient time between complete stages. Each index must finish all 30 documents. Failed/incomplete indexes are preserved and cannot be silently resumed into a completed frozen snapshot. If quota is too small, stop before indexing and report feasibility as blocked.

Run each line separately. Inspect captured extraction/negation fidelity and ledger state before proceeding to the next operation.

```powershell
& $python -B -m graphconflictbench.cli gemini-control status --policy $policy

& $python -B -m graphconflictbench.cli index --config $config --worker-python $python --dataset $dataset --split pilot --condition conflict --output-dir indexes/gemini/stratified-v1-20261115/conflict
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy

& $python -B -m graphconflictbench.cli run --config $config --worker-python $python --dataset $dataset --split pilot --condition conflict --index-dir indexes/gemini/stratified-v1-20261115/conflict --output-dir runs/gemini/stratified-v1-20261115/conflict --budget 4096 --prompt configs/prompts/shared_generation.txt
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy

& $python -B -m graphconflictbench.cli index --config $config --worker-python $python --dataset $dataset --split pilot --condition control --output-dir indexes/gemini/stratified-v1-20261115/control
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy

& $python -B -m graphconflictbench.cli run --config $config --worker-python $python --dataset $dataset --split pilot --condition control --index-dir indexes/gemini/stratified-v1-20261115/control --output-dir runs/gemini/stratified-v1-20261115/control --budget 4096 --prompt configs/prompts/shared_generation.txt
& $python -B -m graphconflictbench.cli gemini-control verify --policy $policy
```

There are six cases and 30 documents per condition. `--split pilot` is intentional; the stratified records are exact pilot copies. Do not add a `--limit` slice of the original 48-case pilot. Never share indexes between conditions or reuse OpenAI vectors merely because both have 1,536 dimensions.

## Output locations

| Artifact | Path |
| --- | --- |
| Configuration/policy/source lineage | `$plan/{lightrag-gemini.yaml,gemini-policy.json,plan.json}` |
| Shared control state | `$plan/gemini-control-v1/{policy.json,ledger.sqlite3}` |
| Provider request/response/error/quota evidence | `$plan/gemini-control-v1/requests/{uuid}/` |
| Index manifest, corpus and raw native build traces | `indexes/gemini/stratified-v1-20261115/{condition}/` |
| Retrievals, raw predictions, parse failures, role-aware/legacy scores | `runs/gemini/stratified-v1-20261115/{condition}/` |
| Per-case native traces and failed/successful generation attempts | `runs/gemini/stratified-v1-20261115/{condition}/cases/{case_id}/{native-N,attempt-N}/` |

HTTP captures contain raw bodies except credential occurrences, non-secret headers, partial/error responses and quota errors. API keys are sent only in the authentication header, excluded from capture and redacted if echoed by an error. Raw vectors are retained before normalization. A $2 paid-equivalent reservation ceiling is shared across all stages, but is not an account-wide invoice guarantee. Missing embedding usage is conservatively charged against that ceiling as an upper bound, never logged as a measured zero-cost request.

Any source, model, policy, configuration or prompt change requires new index/run versions. Preserve the existing ledger's consumed/reserved allowance when planning a retry or migration; never reset it silently. A 429, missing/inconsistent generation usage, expired eligibility or model rerouting requires operator review. No automatic quota-unfreeze/tier-upgrade or budget migration is implemented.
