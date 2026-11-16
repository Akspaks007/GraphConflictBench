# Subsequent approved live smoke — commands only, not executed

Run from the repository root in PowerShell. No paid execution is authorized by preparation of this file. First review the final 12-case worksheet and approve the model, stratified subset, metadata allowlist, unchanged packing policy, completion cap and USD 2 policy.

The final inputs supersede the draft proposal at this directory's root. Use `final-plan/real-smoke.v2.yaml` and `stratified-smoke-v2/`, not the earlier default smoke input. The policy state directory and live index/run paths below are still uninitialized/uncreated.

## Variables and offline checks

```powershell
$cliPython = (Resolve-Path .venv-lightrag/Scripts/python.exe).Path
$workerPython = $cliPython
$plan = 'results/step4-validity-v2-20261115/final-plan'
$config = "$plan/real-smoke.v2.yaml"
$policy = "$plan/provider-policy.v2.json"
$dataset = 'results/step4-validity-v2-20261115/stratified-smoke-v2'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'

& $cliPython -B -m graphconflictbench.cli healthcheck --config $config --worker-python $workerPython
& $cliPython -B -m graphconflictbench.cli audit --dataset $dataset
& $cliPython -B -m graphconflictbench.cli index --config $config --worker-python $workerPython --dataset $dataset --split pilot --condition conflict --output-dir indexes/live/smoke-step4-v2-20261115/conflict --dry-run
```

The healthcheck checks installed native provenance, not API access. `--dry-run` prints arguments, makes no provider call and does not validate credentials. The final config and policy have separately passed schema/hash validation.

Provision `OPENAI_API_KEY` outside logs and command text after paid approval. Do not print it. This policy permits only `https://api.openai.com/v1`; unset/resolve any incompatible `OPENAI_BASE_URL` before proceeding. No custom proxy/provider is silently substituted. Both the native subprocess and generation process use the same frozen policy and ledger.

## Initialize the one shared ledger, after approval

```powershell
& $cliPython -B -m graphconflictbench.cli provider-control init --policy $policy
& $cliPython -B -m graphconflictbench.cli provider-control verify --policy $policy
```

Initialization itself is offline. It refuses to reset an existing state directory. Never delete/reinitialize it to obtain a second $2 allowance. To continue an interrupted run, use `status`/`verify` against this same ledger and reconcile unknown reservations with billing. New dataset/index/run directories do not imply a new spending allowance.

## Paid operations — separate operator checkpoints

Execute each line separately and inspect its logs, provider capture and ledger before the next operation. Do not use `smoke-adapters` for this first paid run because it automatically proceeds across conditions.

```powershell
& $cliPython -B -m graphconflictbench.cli index --config $config --worker-python $workerPython --dataset $dataset --split pilot --condition conflict --output-dir indexes/live/smoke-step4-v2-20261115/conflict
& $cliPython -B -m graphconflictbench.cli provider-control verify --policy $policy

& $cliPython -B -m graphconflictbench.cli run --config $config --worker-python $workerPython --dataset $dataset --split pilot --condition conflict --index-dir indexes/live/smoke-step4-v2-20261115/conflict --output-dir runs/live/smoke-step4-v2-20261115/conflict --budget 4096 --prompt configs/prompts/shared_generation.txt
& $cliPython -B -m graphconflictbench.cli provider-control verify --policy $policy

& $cliPython -B -m graphconflictbench.cli index --config $config --worker-python $workerPython --dataset $dataset --split pilot --condition control --output-dir indexes/live/smoke-step4-v2-20261115/control
& $cliPython -B -m graphconflictbench.cli provider-control verify --policy $policy

& $cliPython -B -m graphconflictbench.cli run --config $config --worker-python $workerPython --dataset $dataset --split pilot --condition control --index-dir indexes/live/smoke-step4-v2-20261115/control --output-dir runs/live/smoke-step4-v2-20261115/control --budget 4096 --prompt configs/prompts/shared_generation.txt
& $cliPython -B -m graphconflictbench.cli provider-control verify --policy $policy
```

There are six cases and 30 documents per condition, so do not add a `--limit` slice of the original pilot. Paired conditions never share an index. `--split pilot` is correct for these copied pilot records.

Stop on a nonzero exit, frozen ledger, missing audit record or unresolved usage. Preserve failures. Do not automatically resume the entire experiment. `--resume` only reuses matching completed work; incomplete index directories require a separately approved fresh path after inspection. A changed source/config/model/prompt requires fresh index/run versions; the existing shared spending ledger must not be reset.

## Outputs

| Output | Path |
| --- | --- |
| Index identity, corpus, native build trace and stores | `indexes/live/smoke-step4-v2-20261115/{condition}/` |
| Aggregate retrievals, raw predictions, legacy and role-aware scores | `runs/live/smoke-step4-v2-20261115/{condition}/` |
| Raw native response/log | `runs/live/smoke-step4-v2-20261115/{condition}/cases/{case_id}/native-{attempt}/` |
| Every attempted generation's prompt, retrieval, error or returned prediction/score | `runs/live/smoke-step4-v2-20261115/{condition}/cases/{case_id}/attempt-{attempt}/` |
| Successful case checksums and canonical final outputs | `runs/live/smoke-step4-v2-20261115/{condition}/cases/{case_id}/` |
| Shared ledger/policy baseline | `results/step4-validity-v2-20261115/final-plan/live-provider-control-v2/{ledger.sqlite3,policy.json}` |
| All provider HTTP attempts | `results/step4-validity-v2-20261115/final-plan/live-provider-control-v2/requests/{uuid}/` |

Each provider attempt contains `request.body`, `request.json` (URL, method and non-secret headers), returned `response.body`/`response.json` if any, and `error.json` if it failed/was denied. Partial returned bytes are retained with `body_complete=false`. The ledger anchors body/metadata hashes and retains unknown reservations. `provider-control verify` checks integrity and reports settled/held amounts in nanodollars (1 USD = 1,000,000,000).

The policy sends a 1536-token completion cap, uses one concurrent native worker and no SDK retries, caps application reservations at $2 and keeps this smoke `benchmark_eligible=false`. The model is the existing GPT-4o mini snapshot, currently deprecated with shutdown scheduled January 14, 2027. Availability and actual response fidelity remain untested. Stop rather than silently migrate if access is unavailable; a replacement needs reviewed compatibility/pricing and fresh artifacts.
