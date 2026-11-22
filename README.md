# GraphConflictBench — implementation through Step 4

This repository implements the requested vertical slice: package and schemas,
typed ontology and shortest-proof verification, a deterministic paired dataset,
and an adapter for the **official LightRAG SDK**. It includes a small shared JSON
generation/scoring seam so retrieval can be exercised end to end.

The included native smoke uses deterministic **test models** for extraction,
embeddings and answers. It tests real LightRAG indexing/retrieval and provenance
handling. These outputs are tagged `benchmark_eligible=false`; they are **not
research results about an LLM or LightRAG accuracy**. An OpenAI-compatible provider
configuration is included, but no paid inference run was performed.

## Quickstart

Use Python 3.11 or newer (verified with 3.12.14). Run from this repository root.
Two environments keep the official architecture dependencies separate.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-locks/core.txt
.venv/bin/python -m pip install -e '.[dev]'
python3 -m venv .venv-lightrag
.venv-lightrag/bin/python -m pip install -r requirements-locks/lightrag.txt
.venv-lightrag/bin/python -m pip install -e .

# Seeds the normal tiktoken cache from bundled, SHA256-verified assets.
.venv/bin/python scripts/cache_tokenizers.py

.venv/bin/python -m graphconflictbench.cli validate-ontology
.venv/bin/python -m graphconflictbench.cli generate --size pilot --resume
.venv/bin/python -m graphconflictbench.cli audit --write-report
.venv/bin/pytest -q tests/unit
.venv/bin/python -m graphconflictbench.cli healthcheck
```

The archive includes the generated pilot, so `generate --resume` verifies and
reuses it. Source files, prompts, models, configuration and native versions are
hashed. Modified inputs require a new output directory. Do not reuse bundled
native snapshots with a different Python/package setup; rebuild fresh snapshots.

Run all 48 pilot queries with test models, building separate conflict/control
indexes (120 documents per index):

```bash
.venv/bin/python -m graphconflictbench.cli smoke-adapters \
  --output-dir results/my-fixture-check

# Opt-in integration test: two real SDK indexes and twelve fixture queries.
GCB_NATIVE_PYTHON="$PWD/.venv-lightrag/bin/python" \
  .venv/bin/pytest -q tests
```

`results/lightrag-pilot/` contains the captured pilot check from this implementation.
The [implementation report](docs/implementation_report.md) describes validation
and limitations. Saved logs preserve the original execution paths for provenance.

## Real models

The Groq configuration uses `GROQ_API_KEY` from the environment or the local
`.env`. Groq supplies chat completions and FastEmbed computes BGE vectors locally.
See [Groq setup and commands](docs/groq_provider.md).

Step 4 v2 requires a frozen provider-capture/spending policy, an explicitly
initialized shared ledger and zero SDK retries. The historical
`configs/architectures/lightrag.yaml` is preserved as a reference and now fails
closed for inference without those controls.

See [the v2 control contract](docs/step4_validity_v2.md) and
[the prepared live commands](results/step4-validity-v2-20261115/LIVE_COMMANDS.md).
They use fresh condition-isolated paths, a stratified 12-case subset copied from
the original pilot, and the installed Windows native environment for model
dependencies. Human signoff and explicit paid-execution approval remain pending.
No paid provider calls have been made. The local $2 reservation ceiling is
conditional on the frozen prices/token bounds; it is not an account-wide billing
guarantee. No automatic full-scale experiment is scheduled.

## What the code enforces

An optional Gemini model provider is now prepared for native LightRAG. See the
[Gemini provider contract](docs/gemini_provider.md) and
[Windows commands](results/gemini-integration-v1-20261115/POWERSHELL_COMMANDS.md).
The CLI loads a repository-root `.env` with `override=False`; the blank
`.env.example` includes `GEMINI_API_KEY=`. Existing OpenAI wrapper/control code
is unchanged. No live Gemini request has been made; model access, project tier,
quotas and the model's December 2026 rerouting deadline remain approval checks.

- Only explicit denial plus a licensed positive proof constitutes a conflict.
  The denial does not count in the 1/2/3 supporting-hop label.
- CONTAINED_IN, SUBREGION_OF and PRECEDES have explicit, typed transitivity.
  Cycles, undefined predicates and type errors are rejected.
- Every support assertion has its own document. Certificates enumerate all
  shortest valid proof edge sets and include ontology/graph hashes.
- Validity intervals are half-open and must overlap across the full proof and
  denial. Missing edges never imply negative claims.
- Families stay in one split. Paired questions are identical. Conditions differ
  in one denied object, and never share an index snapshot.
- Native indexing receives only text, neutral document IDs and file paths; it
  receives no labels, canonical graph, proof sets or case metadata.
- Retrieved chunks and native graph rows are saved. Quotes map to canonical
  assertions only on exact source-text matches. Ambiguous mappings stay unmapped.
- Final prompts contain generic rules and captured evidence, without gold
  witnesses. A `cl100k_base` token cap applies to the actual JSON evidence envelope.
- A strict graph-field allowlist excludes build timestamps and gold metadata;
  raw native responses remain in create-once audit trace directories.
- Role-aware localization metrics accompany the unchanged legacy metrics.
- Raw responses and parse errors are retained; malformed JSON is not repaired
  into a successful answer. Detection and localization are scored separately.
- Exclusive locks, atomic writes, checksums and per-case completion markers
  protect concurrent runs and make checksum-matching resume idempotent.

## Scope and layout

`src/graphconflictbench/` holds the implementation. `configs/` contains ontology,
models and prompt settings. `data/generated/pilot/` contains 24 families/48 cases,
144 unique source documents and separate corpus exports. `tests/fixtures/` holds
12 manually specified logical cases. `docs/` records the protocol, decisions and
environment. `requirements-locks/` pins the two environments.

The research-plan PDF's 240-case full target is available as `generate --size
full`; the handbook's 360-case alternative is `--size handbook-full`. Neither is
an approved/frozen final study. The delivered dataset is the 48-case pilot.

HippoRAG 2, PathRAG, Microsoft GraphRAG, oracle ablations, full statistical
evaluation, resolution and a dashboard are outside this delivery. The CLI exposes
only implemented commands; use `--help` and subcommand `--help` for details.

