# Groq with native LightRAG

Set `GROQ_API_KEY` in the repository-root `.env` or the shell. The shell takes
precedence. Chat requests use Groq's OpenAI-compatible endpoint with
`openai/gpt-oss-20b`. FastEmbed runs the 384-dimensional BGE small English model
locally and caches its public weights under `.venv-lightrag/fastembed-cache`.
Allow the first model download when setting up the environment. This
configuration is for integration runs and uses its own indexes.

To rotate keys, set `GROQ_API_KEYS` to an ordered comma-separated list
in `.env`, for example `GROQ_API_KEYS=first_key,second_key,third_key`.
The populated list takes precedence over `GROQ_API_KEY`. Include the existing
key at the position where you want to use it. Keep the same list and order
across workers for a run. One SQLite counter in the shared ledger assigns each
outbound request its next key and wraps around at the end. Groq measures
quotas at the organization level, so keys in the same organization share
the same allowance. A rate-limit failure still freezes the ledger.

From the repository root in PowerShell, after setting up the native environment
and seeding the tokenizer cache as described in the README:

```powershell
$python = (Resolve-Path '.venv-lightrag/Scripts/python.exe').Path
$config = 'configs/architectures/lightrag-groq.yaml'
$policy = 'configs/architectures/groq-policy.json'
$env:PYTHONUTF8 = '1'
$env:TIKTOKEN_CACHE_DIR = Join-Path (Get-Location) '.venv/tokenizer-cache'

uv pip install --python $python -e '.[groq]'
& $python -c "from fastembed import TextEmbedding; TextEmbedding(cache_dir='.venv-lightrag/fastembed-cache', threads=1)"
& $python -m graphconflictbench.cli healthcheck --config $config --worker-python $python
if (-not (Test-Path 'runs/groq-provider-control-v1')) {
    & $python -m graphconflictbench.cli provider-control init --policy $policy
}
& $python -m graphconflictbench.cli provider-control verify --policy $policy
```

Initialize the ledger once. It shares a $2 application reservation cap across
chat calls, using the published rates in the frozen policy. Account quotas
apply separately. The client sends each request once and preserves HTTP
failures in the ledger.

For a paced run with multiple keys, run
`& $python scripts/run_groq_pilot.py`. It waits
between uses of each key, indexes in checkpointed batches, and resumes completed
work when repeated with the same output path. The interval is per key, so only
use it to aggregate capacity when the keys have separate quota buckets.
The script uses 30 seconds between index calls on the same key and 60 seconds
between scoring calls. Use `--evidence-budget 3072` for the observed 8,000 TPM
bucket. The reduced budget writes a separate scoring directory and reuses any
complete indexes.

After a captured 429, wait for the affected quota to refill and run
`provider-control recover-groq-rate-limit --policy $policy` before resuming.
Recovery verifies the captured response and records the recovery in the
existing ledger. Previous usage, reservations and failed requests are retained.
For a captured Groq token-size HTTP 413, the oversize recovery script checks
the saved response and records the reduced budget before reopening the ledger.

For the bundled 48-case pilot, run each index and its evaluation in turn.
Use a fresh output root and stop if a command fails.

```powershell
$root = 'runs/groq-pilot-v1'
foreach ($condition in @('conflict', 'control')) {
    $index = "$root/indexes/$condition"
    & $python -m graphconflictbench.cli index --config $config --worker-python $python --condition $condition --output-dir $index
    if ($LASTEXITCODE -ne 0) { break }
    & $python -m graphconflictbench.cli run --config $config --worker-python $python --condition $condition --index-dir $index --output-dir "$root/results/$condition"
    if ($LASTEXITCODE -ne 0) { break }
    & $python -m graphconflictbench.cli provider-control verify --policy $policy
    if ($LASTEXITCODE -ne 0) { break }
}
```
