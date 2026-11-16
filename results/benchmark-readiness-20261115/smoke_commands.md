# Proposed real-provider smoke commands — NOT EXECUTED

These are existing CLI operations, not a new evaluator. Commands assume PowerShell at the repository root. Do not run the paid section until human review, timestamp-proxy remediation, model/provider choice, response capture and spending enforcement are approved. The native environment is used for CLI orchestration because core does not currently contain the model extras. Native indexing/retrieval still runs through the existing subprocess worker.

## Prepared inputs

The following offline commands have already been executed. They generated a separate smoke snapshot; they did not alter the original pilot. Repeat only into a new path, or use `--resume` solely for the identical checksum-matching dataset.

```powershell
.\.venv\Scripts\python.exe -B -m graphconflictbench.cli generate --size smoke --output-dir results/benchmark-readiness-20261115/smoke-dataset
.\.venv\Scripts\python.exe -B -m graphconflictbench.cli audit --dataset results/benchmark-readiness-20261115/smoke-dataset --write-report --output-dir results/benchmark-readiness-20261115/smoke-audit
```

This is 12 cases: six per condition, two per condition at each hop depth. There are 30 documents per condition. It omits PRECEDES and is not held out from the pilot. Full family documents, not a `--limit` slice of the pilot, form each index.

## Offline environment and dry-run commands

```powershell
$cliPython = (Resolve-Path .venv-lightrag/Scripts/python.exe).Path
$workerPython = $cliPython
$configPath = 'results/benchmark-readiness-20261115/real-smoke.proposed.yaml'
$datasetPath = 'results/benchmark-readiness-20261115/smoke-dataset'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'

& $cliPython -B -m pip check
& $cliPython -B -m graphconflictbench.cli healthcheck --config $configPath --worker-python $workerPython
& $cliPython -B -m graphconflictbench.cli audit --dataset $datasetPath
& $cliPython -B -m graphconflictbench.cli index --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition conflict --output-dir indexes/live/smoke-readiness-20261115-v1/conflict --dry-run
& $cliPython -B -m graphconflictbench.cli run --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition conflict --index-dir indexes/live/smoke-readiness-20261115-v1/conflict --output-dir runs/live/smoke-readiness-20261115-v1/conflict --dry-run
```

`healthcheck` verifies installed distribution metadata and commit, not provider access. `--dry-run` prints argument selection and returns before configuration/provider validation; it does not estimate cost or test credentials. The review's additional schema validation of the proposal is recorded in `validation.json`.

## Paid commands for approval only

Provision the dedicated API key outside logs and command text. `.env.example` is not automatically loaded by this CLI. Do not include secrets in the review artifacts. If a reviewed hard-cap/logging gateway is used, `OPENAI_BASE_URL` must route both native subprocess and final generation to it. No concrete gateway endpoint or account budget is configured by these commands.

The paths below are reserved for a future fresh run and have not been created. If any input/source/config/model changes, choose another version suffix and regenerate/review the proposal. Do not reuse the delivered fixture indexes or overwrite a failed attempt. Never point indexing at the human-review report folder.

Run conflict indexing first, inspect native build logs, source/negation fidelity and settled usage, then run conflict generation. Inspect raw outputs/errors before proceeding to control. All four commands can incur charges.

```powershell
# After explicit paid-run approval and completion of all prerequisites:
& $cliPython -B -m graphconflictbench.cli index --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition conflict --output-dir indexes/live/smoke-readiness-20261115-v1/conflict

& $cliPython -B -m graphconflictbench.cli run --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition conflict --index-dir indexes/live/smoke-readiness-20261115-v1/conflict --output-dir runs/live/smoke-readiness-20261115-v1/conflict --budget 4096 --prompt configs/prompts/shared_generation.txt

& $cliPython -B -m graphconflictbench.cli index --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition control --output-dir indexes/live/smoke-readiness-20261115-v1/control

& $cliPython -B -m graphconflictbench.cli run --config $configPath --worker-python $workerPython --dataset $datasetPath --split pilot --condition control --index-dir indexes/live/smoke-readiness-20261115-v1/control --output-dir runs/live/smoke-readiness-20261115-v1/control --budget 4096 --prompt configs/prompts/shared_generation.txt
```

No `--limit` is needed: the prepared dataset already has six cases per condition. CLI `--split pilot` is correct even though the directory is named smoke. A single `smoke-adapters --config ... --dataset ... --output-dir ...` command also exists, but runs both conditions without a manual checkpoint; the staged commands are proposed for the first paid use.

## Expected output paths

| Output | Path pattern |
| --- | --- |
| Frozen corpus and index identity | `indexes/live/smoke-readiness-20261115-v1/{condition}/corpus.jsonl`, `index_manifest.json` |
| Native build request/response/log | `indexes/live/smoke-readiness-20261115-v1/{condition}/build/{request.json,response.json,native.log}` |
| Native document/chunk/graph/vector stores | `indexes/live/smoke-readiness-20261115-v1/{condition}/native/` |
| Aggregate retrievals, responses, scores and summary | `runs/live/smoke-readiness-20261115-v1/{condition}/{retrieval.jsonl,predictions.jsonl,scores.jsonl,summary.json,run_manifest.json}` |
| Exact final prompt and raw generation text/parse error | `runs/live/smoke-readiness-20261115-v1/{condition}/cases/{case_id}/{prompt.json,prediction.json}` |
| Raw native retrieval response and log | `runs/live/smoke-readiness-20261115-v1/{condition}/cases/{case_id}/native-1/{request.json,response.json,native.log}` |
| Per-case retrieval, score and completion checksum | `runs/live/smoke-readiness-20261115-v1/{condition}/cases/{case_id}/{retrieval.json,score.json,complete.json}` |
| Additional required live capture/cost ledger | Gateway/guard path to be approved; existing CLI does not create a complete raw extraction-response ledger |

Successful build responses contain indexing usage; native retrieval responses contain keyword/embedding usage; final `prediction.json` contains generation usage. Aggregate summaries do not calculate cost. Failed native work can leave logs without a response/usage artifact. Preserve it and reconcile external billing before considering a separately approved fresh attempt.

## Acceptance checklist for the subsequent run

- Both indexes report 30 processed documents and are condition-isolated.
- Raw extraction/gleaning requests, responses and errors are retained externally or by the separately approved capture change.
- Timestamps and other unapproved volatile metadata do not reach final prompts; no canonical graph/proofs/labels enter indexing or generation.
- Manually inspect all 12 cases for exact source names, negation, citations and support/opposing roles. Record every failure; a smoke need not attain perfect accuracy.
- Account for every request in the cost ledger, including embeddings, failures and in-flight reservations, under the agreed USD 2.00 hard cap.
- Preserve `benchmark_eligible=false`, raw JSON/schema failures and the distinction between plumbing outcomes and research findings.
