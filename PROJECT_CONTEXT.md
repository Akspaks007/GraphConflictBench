# GraphConflictBench shared project context

Updated 24 November 2026. The repository has a complete native LightRAG pilot,
working Groq integration, and two reusable saved indexes. Each additional
architecture needs its own native indexing and retrieval adapter. Use the
[adapter handoff prompt](docs/adapter_handoff_prompt.md) to start that work.

## Benchmark contract

GraphConflictBench tests whether a retrieval and generation pipeline can detect
an explicit contradiction and cite the source statements that prove it. For
example, two source documents establish A inside B and B inside C. A third
document denies A inside C. The matched control keeps the question and support
chain and changes the denial to A outside D. Proof depth counts the supporting
edges, so the example has two hops.

- The frozen synthetic pilot uses seed 42 and contains 24 matched pairs, eight
  pairs at each depth of one, two and three hops. There are 120 documents per
  condition and 144 unique source documents overall.
- The ontology licenses transitivity for `CONTAINED_IN`, `SUBREGION_OF` and
  `PRECEDES`. A conflict requires an explicit denial of a conclusion that
  follows from a valid positive chain. Check relation types and overlapping
  validity intervals. Missing evidence leaves the claim unknown.
- Keep conflict and control corpora in independent indexes. Use the frozen
  corpus exports under `data/generated/pilot/corpora/pilot/`. Index only source
  text and neutral IDs or paths. The evaluator uses canonical assertions,
  labels and proof certificates after retrieval to check source alignment
  and score responses. Keep those fields out of model-visible data.
- Use the shared generation prompt and strict JSON parsing. Preserve raw
  retrieval, raw model output, and failures locally. Align citations to exact
  attributed source statements. Report detection, full-proof availability,
  and role-aware proof citation separately, including invalid responses.

[Protocol](docs/protocol.md) · [Dataset card](docs/dataset_card.md) · [Reasoner](src/graphconflictbench/reasoner.py) · [Scorer](src/graphconflictbench/metrics.py)

## Groq and execution

- `src/graphconflictbench/providers.py` selects the provider. The Groq wrapper
  uses `openai/gpt-oss-20b` for chat and local FastEmbed
  `BAAI/bge-small-en-v1.5` for 384-dimensional vectors. Existing OpenAI,
  Gemini and fixture routes are available through their own configs.
- Put one Groq credential in `GROQ_API_KEY` or an ordered comma-separated
  pool in `GROQ_API_KEYS` in the ignored repository-root `.env`. A populated
  pool takes precedence. Rotation is shared across workers through SQLite.
  Quota is per Groq organization. Keep credentials, provider captures, the
  SQLite ledger and local attempt directories out of Git.
- The frozen Groq policy has a shared $2 application reservation cap and
  zero SDK retries. Keep failed attempts and prior reservations when
  recovering. The live runner uses 10-document checkpoints and pauses between
  requests on the same key. The verified run used 30 seconds during indexing
  and 60 seconds during scoring.
- The final run used **3,072 `cl100k_base` tokens for the packed evidence
  envelope** in both conditions after an oversized request at 4,096. This
  evidence budget is distinct from Groq's request limits and reported usage.
  Use 3,072 for a like-for-like run and record any differences in model,
  embedding, packing or retrieval settings.

[Groq setup and recovery](docs/groq_provider.md) · [Groq config](configs/architectures/lightrag-groq.yaml) · [Shared prompt](configs/prompts/shared_generation.txt)

## LightRAG pilot baseline

The final provisional Groq run scored all 48 cases with a valid response on
42 of 48. It correctly detected 5 of 24 conflicts and cleared all 24 controls.
None of the conflict answers cited a complete exact proof with the correct
supporting and opposing roles.

| Hops | Conflicts detected | Missed | Invalid | Full proof delivered | Controls cleared |
|---|---:|---:|---:|---:|---:|
| 1 | 2/8 | 2 | 4 | 6/8 | 8/8 |
| 2 | 3/8 | 4 | 1 | 3/8 | 8/8 |
| 3 | 0/8 | 7 | 1 | 0/8 | 8/8 |

Both native LightRAG indexes are checked into `indexed_graphs/groq-pilot/`.
The restore script checks the source, configuration, native SDK and BGE
cache revision, then prepares local CLI indexes without running indexing
again. The original index has 120 documents per condition. Use a fresh
snapshot and a distinct output path for another architecture. Local full
traces for this scored run are under
`runs/groq-pilot-checkpointed/results-3072/` when available.

[Saved indexes and restore instructions](indexed_graphs/README.md) · [Published hop results](indexed_graphs/groq-pilot/results_by_hop.json)

## Current scope and shared updates

The original delivery covered LightRAG through Step 4. HippoRAG 2, PathRAG and
Microsoft GraphRAG are possible follow-on adapters. Start with the one named in
the new task. Each implementation should expose its native capabilities and
record unavailable evidence or provenance fields explicitly. Full statistical
evaluation, resolution, oracle ablations and a dashboard remain follow-on work.

Update this file in the same change as each provider or adapter integration and
each completed evaluation. Record the architecture and upstream revision,
entry points and dependencies, dataset and settings, verification actually
run, results by hop with denominators, artifact paths, and open blockers.
Keep the detailed protocol, provider docs, raw captures and run manifests as
their respective sources of truth. On this Windows setup, the existing
symlink unit test needs permission Windows did not grant. Report it separately
from project regressions.
