# Prompt for adding a GraphConflictBench adapter

Copy the prompt below into a coding agent session opened at the repository root
and replace `[ARCHITECTURE]` with the one your team wants to implement.

---

Extend **GraphConflictBench** with a native adapter for **[ARCHITECTURE]**.
The Groq provider and the first architecture, LightRAG, are already wired and
tested. Read `AGENTS.md`, `PROJECT_CONTEXT.md`, `docs/protocol.md`,
`docs/groq_provider.md`, and `indexed_graphs/README.md` before making changes.
The shared context has the frozen pilot, baseline results, and environment notes.

## Implement one architecture end to end

1. Inspect the selected project's upstream code and native indexing and query
   entry points. Record its version or commit, dependency requirements, and
   how to verify the installed runtime. Keep architecture dependencies
   isolated where the upstream packages require it.
2. Follow the adapter interface in `src/graphconflictbench/adapters/base.py`
   and the runner's existing contracts for health check, indexing, retrieval
   and audit traces. Connect the new architecture to the normal CLI through
   its own config and selection path. Preserve the LightRAG defaults and
   keep the native implementation for the selected architecture.
3. Reuse the existing Groq provider and documented `.env` variables. Use
   `openai/gpt-oss-20b` and local 384-dimensional BGE embeddings wherever the
   native architecture supports those callbacks. Record any native model or
   embedding requirement and explain its effect on comparisons. Keep the
   shared request ledger, secret redaction, pacing and failure capture in the
   live path. Confirm quotas and spend settings before live execution.
4. Use the frozen 48-case pilot with independent conflict and control corpora.
   Build each architecture's own native indexes under fresh, distinct paths.
   Give the indexer only source text and neutral IDs or paths. Use the same
   question, shared final-generation prompt and 3,072-token evidence budget
   as the Groq LightRAG baseline for comparable scoring. Pass gold labels,
   canonical graph edges and proof certificates only to grading code.
5. Save native retrieval, source provenance, exact-quote citation mappings,
   raw responses and parsing failures. Expose unsupported native fields as
   unavailable. Keep whole-proof retrieval, detection, invalid responses
   and exact role-aware citations separate in the score report. Provide
   counts and denominators for each hop depth and condition.

## Verify and hand off

- Run unit tests, lint and a real native SDK integration test with fixture
  callbacks first. Demonstrate index reuse or restart from a verified
  checkpoint. Mark fixture outputs as `benchmark_eligible=false`.
- For an authorized live pilot, run both conditions and preserve incomplete
  attempts if a provider limit interrupts the work. Report the exact dataset,
  model, prompt, evidence budget, native retrieval settings and usage. Report
  measured results only and identify any stages that remain incomplete.
- Keep reusable, verified index archives in a distinct architecture folder
  under `indexed_graphs/` when preparing Git-shareable artifacts. Include
  checksums and restore instructions. Keep credentials, raw API captures,
  local ledgers and private paths out of published artifacts.
- Update `PROJECT_CONTEXT.md` before finishing. Add the adapter's upstream
  version, commands, tests, scope, known limitations and verified result and
  artifact paths. Keep the LightRAG baseline available for comparison.
