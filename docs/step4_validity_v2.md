# Step 4 validity and provider controls (v2)

This is hardening of the first LightRAG integration, not implementation Step 5 or another architecture. The recorded scope decisions in `decisions.md` stand. No pilot assertions, labels, proof depths or certificates changed.

The authoritative new review, verification results and future live commands are under `results/step4-validity-v2-20261115/`. Historical source and all 739 original artifacts are preserved in `historical-step4.zip`; the original `ARTIFACT_MANIFEST.json` is still the baseline, not a manifest of the edited working tree.

## Model evidence contract

Native indexing and retrieval remain official SDK operations. Raw native responses are preserved in fresh trace directories that cannot be overwritten. Final model envelopes use an allowlist at both normalization and prompt construction:

- Entities: entity name, type, description and neutral source filenames.
- Relationships: source/target entity names, keywords, description and neutral source filenames.
- References: numeric reference ID and neutral source filenames.

Only string values are admitted. Unknown fields, nested values, timestamps, cache/chunk IDs, native weights and build metadata are excluded. Model-visible paths must be neutral `D<20 hex>.txt` names (or their native `<SEP>` aggregation). Canonical assertion mappings and gold metadata never enter the evidence envelope. Native description strings remain untrusted content, not verified facts or directed proofs.

The 4096-token cap and packing order remain unchanged: source chunks, entities, relationships, references, each in native order. Filtering changes the size of rows and therefore which later rows fit; that is an explicit presentation-version change and requires fresh snapshots. A different source/graph allocation is a proposed controlled protocol change, not enabled here.

## Metrics

Legacy `localization_f1` and `exact_proof_set` retain their union-of-citations behavior for comparison. New v2 fields separately score support and opposing assertion IDs, role-tagged F1 and exact role-aware proof sets. Each reported conflict must carry a complete correctly assigned witness to pass the exact metric; splitting a witness over conflict objects or adding an unmappable quotation fails it. Role-aware mapping checks all delivered chunks of a document, rather than only its final chunk. Explanation quality and source truth are still not scored.

## Provider control

Real-provider use requires an initialized, SHA256-frozen policy and a shared persistent ledger. The former unguarded live configuration now fails closed. New live commands use the installed native environment so that the OpenAI/NumPy model dependencies are available. SDK/transport retries are disabled; every upstream/manual retry that reaches the client is captured and charged/reserved separately.

At the HTTP boundary, exact JSON request bodies, response bodies (after HTTP decompression), non-secret headers, partial responses and errors are written once. Authorization/cookie/API-key headers are excluded. SQLite transactions reserve worst-case request costs before network dispatch across all participating processes. Missing/invalid usage freezes the ledger; connection/HTTP failures keep their full reservation. Crashed reservations are never automatically refunded. New per-attempt prompt/retrieval/error files survive generation failures and resumes.

The policy supports only priced plain-text OpenAI chat completions and text embeddings. It rejects unknown models, origins, endpoints, options and multimodal/tool/streaming requests. A per-call completion cap is sent explicitly. The $2 ceiling is an application reservation ceiling under the frozen prices and conservative byte-based input bounds, not a promise about an entire account's invoice. External key use, price changes, provider billing/tokenization anomalies, taxes and manual state tampering are outside it. Use a dedicated key/project and a provider-enforced limit as additional controls. Local files are create-once/checksummed by this code; they are not hardware WORM storage.

The prepared six-family smoke subset copies existing pilot records into a fresh snapshot with two families per depth and two per predicate. It is not held out. Human signoff and explicit approval of the model, subset, presentation version and paid execution remain required.
