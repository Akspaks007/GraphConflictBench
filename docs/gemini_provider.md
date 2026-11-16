# Optional Gemini model provider for Step 4 LightRAG

This adds a model provider to the existing native LightRAG integration, not a new GraphRAG architecture. The canonical dataset, ontology, proofs, shared generation prompt, metadata allowlist, role-aware metrics and paired-condition isolation are unchanged.

Use the integration report and exact Windows commands in `results/gemini-integration-v1-20261115/`. Only the final `proposed-plan-v3/` is the prepared proposal; it remains blocked on project eligibility. The v2 stratified input is reused at `results/step4-validity-v2-20261115/stratified-smoke-v2/`.

## Provider boundary

`providers.model_provider()` selects fixture, unchanged OpenAIModels, or GeminiModels. The official LightRAG worker still runs native extraction, `ainsert` and hybrid `aquery_data`; Gemini only supplies the LLM/embedding callbacks and the shared final generation call. Gemini uses the documented REST `generateContent` and `embedContent` methods through httpx for explicit request accounting/capture. The already-installed Google SDK is not needed by this route. There are no hidden discovery, countTokens, file, tool, grounding, billing or retry calls.

The proposed language model is `gemini-2.5-flash`. Generation uses temperature 0, one candidate, a 1,536-token output cap and disabled thinking. Native keyword JSON requests map to Gemini's JSON MIME option; final predictions retain the fixed shared prompt and strict parsing rather than repair. Blocked/empty/truncated responses remain captured; no successful answer is selected by retrying. Returned model versions are recorded and non-2.5-Flash versions rejected. Calls are blocked from December 1, 2026 to prevent the documented automatic reroute.

Embeddings use `gemini-embedding-001`, explicit 1,536 output dimensions, L2 normalization and `SEMANTIC_SIMILARITY` on every index/query callback. This symmetric task avoids guessing a query/document role from native callback internals. Other reviewed recommended dimensions (768/3072) require a different frozen configuration and fresh indexes. Vectors must have the exact expected shape, finite entries and nonzero norm. The native maximum embedding input is 2,048 tokens; a conservative byte-bound guard rejects oversized texts without truncating them. No OpenAI vector store is reused.

## Secrets and dotenv

The CLI and native worker load the explicit repository-root `.env` via python-dotenv with `override=False` and interpolation disabled. The parent's environment is inherited by the worker; its temporary CWD is not searched for another `.env`. Explicit shell values win. Only `GEMINI_API_KEY` supplies Gemini authentication; `GOOGLE_API_KEY` is not a fallback. The user-owned `.env` is not rewritten, displayed, hashed or archived. `.gitignore` ignores `.env`/`.env.*` and permits only `.env.example` as a public blank template.

Authentication headers are excluded from audit files. Registered credential values and their URL/JSON-escaped forms are redacted from diagnostics, exception messages and response bytes. A response that echoes a credential is captured redacted and stops further requests. Raw unredacted keys do not enter model prompts, configs, usage records, index keys or manifests. Readiness verification only reports a boolean credential-leak scan; it never records credential values or fingerprints.

python-dotenv 1.2.4 was added to the core lock and is already pinned/installed in the native lock. The project declares it as a base dependency. The optional `gemini` extra declares httpx and NumPy; both are already installed in the native environment used by the commands.

## Gemini-specific controls

Gemini has a separate strict policy and SQLite quota table. Its paid-equivalent rates are the published Gemini 2.5 Flash text rates and Embedding 001 rate, not OpenAI prices or presumed free pricing. Even human-confirmed free-tier projects use nonzero conservative reservations. The actual account invoice/free eligibility cannot be inferred from this client.

An eligibility/reference/date and reviewed active quotas are required before ledger initialization or provider creation. Attestations expire after seven days, and the fixed routing deadline is earlier if applicable. Policies are immutable Pydantic records, hashed into the adapter configuration; changing them invalidates snapshot reuse.

One transaction reserves spending and lifetime/rolling-day/rolling-minute quota before dispatch. Defaults are at most 500 requests total, 200 per rolling 24h, at least 31 seconds apart, 40,000 conservative input-bound units/minute and a $2 paid-equivalent ceiling. Operators must lower them to fit their actual project. Google quotas are per project and can be consumed by other keys/applications. A 429 retains its body and Retry-After, freezes the ledger and never retries/upgrades a tier automatically. Unknown failures keep their entire reservation. Missing embedding usage is marked unknown and consumes the full upper bound; missing/invalid generation usage freezes the ledger.

For Gemini index/query subprocesses only, the timeout allows headroom for policy-mandated waits: `1800 + min(total request cap, rolling-day cap) * (minimum spacing + 180)` seconds. This does not increase any provider allowance. OpenAI, fixture and metadata-healthcheck operations retain their existing 1,800-second timeout.

This is conditional application protection, not an unconditional account spending guarantee. Prices/token bounds/provider usage must remain valid; external traffic, taxes, billing anomalies and manual state tampering are outside it. Local captures are create-once and checksummed, not hardware WORM storage. Always use fresh artifact paths and retain the same consumed allowance across stages and any separately reviewed recovery.
