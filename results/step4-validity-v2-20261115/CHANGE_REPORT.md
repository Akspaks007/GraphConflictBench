# Step 4 experimental-validity hardening — v2

15 November 2026, Asia/Kolkata. This work stays within the first native LightRAG integration. No paid API request, original pilot regeneration, gold-label/proof-depth edit, additional architecture or Step 5 work occurred.

## Outcome and materials

The timestamp field proxy is removed from new model-visible envelopes; role-aware localization is implemented alongside the legacy metric; HTTP capture and a cross-process pre-dispatch spending ledger are implemented and tested offline. The original packing order and 4,096-token retrieval-evidence cap remain unchanged. Human review and real-provider behavior remain unverified.

| Material | Location |
| --- | --- |
| Final twelve-case worksheet with actual questions, full documents, denials, ordered shortest proofs, labels and ambiguities | [HTML](final-plan/human_review_smoke12.html), [Markdown](final-plan/human_review_smoke12.md), [CSV](final-plan/human_review_smoke12.csv) |
| Fresh stratified input and original-record lineage | [dataset manifest](stratified-smoke-v2/dataset_manifest.json) |
| Final guarded live configuration | [real-smoke.v2.yaml](final-plan/real-smoke.v2.yaml) |
| Frozen price/cap/capture policy | [provider-policy.v2.json](final-plan/provider-policy.v2.json) |
| Exact subsequent approved live commands and output paths | [LIVE_COMMANDS.md](LIVE_COMMANDS.md) |
| All 48 rebuilt prompts and filtered evidence | [prompt-replay-v2](final-plan/prompt-replay-v2/) |
| Packing/leakage diagnostic | [replay-report.json](final-plan/replay-report.json) |
| Final test, audit, lineage and preservation results | [verification.json](verification.json) |
| Original 739-file baseline plus original artifact manifest | [historical-step4.zip](historical-step4.zip) |

The root-level draft worksheet/config generated earlier in this task is retained as preparation history. It uses the old default smoke input. **Only `final-plan/` with `stratified-smoke-v2/` is proposed for the subsequent live smoke.** No live state directory, index or run has been initialized.

## Changes to model-visible evidence

`prompts.model_visible_graph()` permits only these native fields:

| Native row kind | Allowlisted fields |
| --- | --- |
| Entity | `entity_name`, `entity_type`, `description`, neutral `file_path` |
| Relationship | `src_id`, `tgt_id`, `keywords`, `description`, neutral `file_path` |
| Reference | numeric-string `reference_id`, neutral `file_path` |

Only string values are admitted. Paths must be neutral `D<20 hex>.txt` names or native `<SEP>` aggregations of those names. Unknown fields and nested objects are dropped. This excludes `created_at`, build/cache identifiers, native source/chunk IDs, weights, gold labels, proof IDs and assertion mappings. The sanitizer is applied before token accounting and again at final prompt construction, so passing an older unsanitized Retrieval object cannot bypass it. Source chunks are retained verbatim and remain untrusted source data. Native descriptions are not promoted to canonical claims or directed proof paths.

The raw response object is never mutated. Native `_call` trace directories are created atomically and cannot be reused. Provider capture files use exclusive create and fsync. Completed run manifests bind native traces by checksum. Original historical prompts, responses and result folders were not edited.

Offline replay of all 48 saved native responses rebuilt 48 new prompts with no volatile/gold metadata fields. It retained the same 1,734 source-chunk occurrences. These are **presentation replays**, not fresh retrievals or model answers. The native fixture test separately rebuilt new SDK indexes and executed 12 queries with fixture models.

## Why relationship rows were omitted

Packing is a greedy prefix of source chunks, followed by entities, relationships and references. The historical final model envelopes contained zero relationship rows even though raw native retrieval returned them. Source chunks and retained entity rows left a median **30 tokens** before relationships (range 0–85); the median smallest relationship-row increment was **108 tokens**. Since relationship rows were tried after entities, none fit. This is an envelope allocation issue, not proof that native LightRAG extracted or retrieved no relationships.

Filtering metadata shrinks rows, but the unchanged loop uses much of the newly available space for more entities. In the v2 replay, the median remaining space before relationships is **18 tokens**; the median smallest relationship increment is **78 tokens**. Five relationship rows fit in five of 48 cases. No source chunk changed or was removed. This limited recovery does not establish native proof-path observability, and no directed paths were invented.

**Controlled proposal, not implemented:** compare the current packing policy with a preregistered 3,072-token source / 1,024-token graph allocation within the same 4,096 total. The graph segment would interleave native relationship/entity rows in native order and retain source attribution; both arms must measure the actual JSON envelope, record omissions and use identical corpora, queries, model, top-k/native token settings and paired isolation. Reserve space without consulting gold witnesses. Measure the tradeoff in complete source-proof delivery before approving a methodology change. Do not silently increase the cap or replace source quotes with gold documents. If the first live smoke retains current packing, explicitly accept its limited relationship exposure.

## Role-aware localization

The legacy `localization_f1` and `exact_proof_set` remain unchanged for compatibility, including their union-of-cited-assertions behavior. New fields are:

- `support_localization_f1` and `opposing_localization_f1`;
- `role_aware_localization_f1` over role-tagged assertion IDs;
- `role_aware_exact_proof_set` and `role_metric_version=2.0`;
- `role_citation_errors` and the run summary's `role_aware_exact_proof_cases`.

Swapping support/opposing lists now scores zero role-tagged F1 and fails role-aware exactness while preserving the old union metric. Each reported conflict object must itself match one shortest support set and its explicit denial. Splitting a witness across objects or adding a quote that maps to no assertion fails exactness. Citation alignment checks both the original source and any one delivered chunk of that document; later chunks no longer hide earlier valid quotes in the new metric. Detection remains separate. These metrics do not judge explanation prose, eliminate all duplication issues or choose which conflicting source is true. Historical score files were not recomputed in place.

## Complete provider capture

All `OpenAIModels` callbacks, whether used for indexing extraction/gleaning/summaries, entity/relationship/source embeddings, retrieval keyword/query embeddings or final generation, use one guarded HTTP client. The worker and separate generator load the same SHA256-frozen policy. The old unguarded configuration fails closed. SDK and transport retries are disabled; any upstream/manual retry reaching dispatch obtains a new reservation and audit record.

For every attempted request, UUID directories retain exact JSON request bytes, URL/method and non-secret headers, returned response bytes/status/headers and errors. Bodies are captured at the HTTP-client boundary after response decompression, not as TLS packets. Authorization/API-key/cookie headers are excluded. Full returned bodies, non-2xx replies, malformed usage and partial response bytes are preserved. A partial transfer is marked `body_complete=false`; an abrupt process kill can leave incomplete records and a held reservation, not a fabricated complete response. A request that never reached the transport has no provider request/response to capture; process/native error logs remain available.

Each generation attempt also retains its prompt, normalized retrieval and returned prediction/score or exception under `attempt-N/`. A later resume writes a new attempt and does not discard the failed context. Raw provider failures need not be parseable benchmark predictions.

The capture files are create-once by this program and their body/metadata hashes are anchored in SQLite. Verification detects missing/changed captures and unregistered request directories. This is not hardware WORM storage or a defense against an administrator altering both files and database. Preserve an external copy of the final manifest/ledger for stronger tamper evidence.

## Spending control and the $2 limitation

The policy caps **settled cost plus all outstanding/uncertain reservations** at **2,000,000,000 nanodollars = USD 2.00**. SQLite `BEGIN IMMEDIATE` serializes reservations across processes. Before actual HTTP dispatch it reserves input cost conservatively using request UTF-8 byte counts plus message-framing allowance, and reserves the full requested output-token maximum. Every LLM call sends `max_tokens=1536`. Embedding text uses a conservative byte bound. Unknown origins/endpoints/models/options and multimodal/tool/streaming requests are rejected.

Successful responses settle at reported usage, priced at the frozen policy; only the unused reservation is released. Missing/inconsistent/out-of-bound usage freezes the ledger. Network/HTTP failures and crashed calls retain the full reservation indefinitely. No automatic refund or ledger reset exists. Policy changes cannot silently increase an initialized ledger's allowance. `provider-control init/status/verify` are offline CLI operations; the actual live ledger remains uninitialized until a separate approval.

Prices rechecked 15 November 2026: [GPT-4o mini](https://developers.openai.com/api/docs/models/gpt-4o-mini) $0.15/M input and $0.60/M output tokens; [text-embedding-3-small](https://developers.openai.com/api/docs/models/text-embedding-3-small) $0.02/M input tokens. The existing low-cost smoke estimate remains approximately **$0.08**, with a planning range **$0.05–$0.30** for 60 document instances, up to 60 gleaning passes, 12 keyword calls, 12 final generations and data-dependent summaries/embeddings. This estimate is not observed usage or a guaranteed cost. No invoice or account balance was queried.

The $2 invariant is an **application-level conditional ceiling**, not an unconditional account invoice guarantee. It assumes the reviewed prices, byte-level text-token bounds, provider completion cap and truthful usage/billing contract. Provider anomalies or changed prices can violate an assumed bound before a response reveals it; the guard freezes subsequent traffic but cannot reverse a charge. Taxes, currency conversion, account-wide calls made outside this client, deliberate file/ledger tampering and a manually created second allowance are not controlled. The guard does not support arbitrary OpenAI-compatible gateways. Use a dedicated project/key and an enforced provider limit as backstops. Official [project guidance](https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform) notes that provider enforcement can lag and exceed its configured limit slightly; alerts alone do not stop requests. No platform limit was changed here.

## Twelve-case human review and selection

The final snapshot copies families `F10000`, `F10001`, `F20000`, `F20002`, `F30001`, `F30002` from the unchanged pilot. Selection was declared by depth/predicate cells rather than fixture outcomes. It gives two families at each depth and two for each predicate; therefore each of the three predicates has two conflict and two control cases. Both conditions have 30 documents. The previous default 12-case smoke omitted PRECEDES; the new proposal resolves that omission with a separately identified input, not a silent change to the original.

Six families cannot cover all nine predicate × depth cells. This small set is for provider plumbing/fidelity and formatting, not a powered study or held-out evaluation: all twelve cases overlap the pilot. Each CSV row contains the full actual question, source-document JSON with verbatim text, ordered proof-path JSON with edge/document IDs, explicit denial, condition/label and possible ambiguities. Markdown/HTML provide the same material for readable review. All reviewer/date/decision fields remain blank.

Human attention remains necessary for fictional rule scope, open-world controls, supporting depth versus denied-object semantics, and the two depth-1 positive/negative endpoint merges in this subset. All source statements, IDs, labels, depths and certificates are exact copies. Review artifacts contain gold information and must never be native indexing or final-generation inputs.

## Verification and preservation

Final verification: **69 unit tests passed**, **9 integration tests passed** (one genuine native SDK test with two new indexes/12 fixture queries plus eight offline HTTP/SDK tests), Ruff passed, and original-pilot plus stratified-input dataset audits passed. Native fixture runs remain `benchmark_eligible=false`. The detailed machine record includes schema checks, CLI dry-runs, leakage checks of all replayed/new native prompts, and original-record lineage.

The tests cover volatile/gold nested metadata, unsafe paths, final-prompt bypass attempts, exact budget measurement, swapped roles, split witnesses, multi-chunk source matching, trace overwrite rejection, failed generation/resume preservation, concurrent/cross-process reservations, policy mismatch, crash holds, malformed usage, blocked dispatch, missing/partial/error responses, raw capture tampering and actual SDK callback coverage. All HTTP tests use explicit offline transports and fake credentials. No paid request is made by the test suite.

Earlier development reports remain preserved. In particular, `integration-final.xml` contains one failing **test expectation**: it expected the SDK to wrap the guard's HTTP-500 RuntimeError. This SDK propagates it directly. The test was corrected to assert the actual RuntimeError and a single captured/held request; `integration-verified.xml` is the passing rerun. Earlier index snapshots and logs were retained and never overwritten.

All historical data/config/prompt/result files still match the original manifest. Expected working-tree changes are implementation/test files and README; their original bytes, together with every other one of the original 739 entries, are preserved in `historical-step4.zip`. Its SHA256 is `d3eb398f31542401d5651f3f4225eee8726be4aaa0ed9df3b731cc0f10bf587c`. The original `ARTIFACT_MANIFEST.json` was not rewritten to conceal these source changes. A new versioned manifest records the current state separately.

## Remaining approvals and limits

1. Complete human signoff of the final twelve cases; disputed cases must be explained, not relabeled to fit outputs.
2. Approve the new stratified input, v2 presentation contract, per-call completion cap and current source-first packing for the smoke, or approve the controlled fixed-total packing comparison before paid use.
3. Approve the priced model/provider and separate paid execution. The existing GPT-4o mini snapshot is deprecated; the [official schedule](https://developers.openai.com/api/docs/deprecations) lists January 14, 2027 shutdown. Access and real extraction/format fidelity remain untested. Do not silently substitute a model.
4. Review the guard's scoped/conditional $2 guarantee and dedicated-project backstops. Initialize the one shared ledger only after the above approvals and never reset it to bypass the allowance.

No additional architecture integration or Step 5 implementation is proposed by these changes. The exact approved-run command sequence is in [LIVE_COMMANDS.md](LIVE_COMMANDS.md).
