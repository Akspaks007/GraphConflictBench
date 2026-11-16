# Decisions and reference reconciliation

Recorded 15 November 2026 (user-facing date in Asia/Calcutta).

1. The user's request authorizes implementation through **Step 4, LightRAG**.
   We interpret that as Section 12's ordered implementation table in the handbook.
   The PDF schedule's fourth work package groups LightRAG/HippoRAG 2, while the
   handbook's Phase 4 concerns shared generation. Those numbering systems do not
   expand the explicit LightRAG endpoint to the other architectures or full study.
2. The handbook includes a ready-made agent prompt that says to stop after
   Phases 0/1 and lists approval gates. That text was treated as an attached
   reference, not the user's operational instruction. It does not override the
   user's request to implement through LightRAG. No additional approval was
   requested for reversible local implementation and tests.
3. Default pilot: handbook's detailed 24-family/48-case paired pilot. The PDF
   suggests a 20-case pilot and a 240-case full set; the handbook proposes 360
   full cases. Preserve the PDF full target as default (120 families), expose the
   handbook full alternative explicitly (180 families), and deliver only the pilot.
   No proof/label semantics were changed to reconcile dataset counts.
4. Gold graph storage is typed JSONL and pure-Python proof search. Neo4j is
   optional in both references and unnecessary for logical correctness. Native
   LightRAG uses its own JSON, NetworkX and NanoVectorDB stores.
5. Separate orchestration/native virtual environments with a JSON subprocess
   boundary. The observed upstream now requires Python >=3.11, so the handbook's
   tentative Python 3.10 setup was updated to >=3.11; verified runtime is 3.12.14.
6. Official upstream: HKUDS/LightRAG, commit
   `f615931d6ab60b179d5347f92a29f75dcff776a6`, installed version 1.5.8, MIT.
   The worker validates installed VCS provenance against this commit before use.
7. No model credentials were supplied. Execute the genuine native SDK with
   deterministic extraction/embedding/answer test models. Clearly exclude those
   outputs from research claims. Provide a separate OpenAI-compatible provider
   route without making paid model calls. Model choices there are provisional.
8. Native query uses `aquery_data()` with hybrid retrieval and explicit graph
   token allowances, leaving room for source chunks. We observed that permissive
   graph defaults can consume the entire context and return no source chunks.
   The envelope retains native data within a separate 4096-token evidence cap.
9. Inference depth is the minimum positive source-backed proof length; denial
   is a separate witness. Exact text spans can justify assertion mappings even
   when native graph paths are not exposed. No native directed paths are invented.
10. The normal tiktoken blob-host request was denied by the environment's proxy.
    A public GitHub mirror supplied bytes matching tiktoken's built-in SHA256
    expectations. Bundled assets seed the normal cache; TLS, proxy and tokenizer
    semantics were preserved. See assets/tokenizers/PROVENANCE.md.
11. Model-visible document/entity/case IDs are neutral hashes. In particular,
    the response `case_id` never contains `conflict` or `control`. The audit reports
    observed pairing checks separately from a trained leakage classifier, which
    has not been run. Human review is pending, not assumed from automatic checks.
12. Future approvals/research choices: human pilot audit, real-model/provider
    and spend settings, adapter fidelity review, final target/power and held-out
    freeze. These do not block delivery of the requested implementation.

