# GraphConflictBench shared project context

Updated 25 November 2026. The repository has native LightRAG and HippoRAG 2
adapters. The LightRAG Groq pilot and its two saved indexes are available as
historical artifacts. Each additional architecture needs its own native index
and retrieval adapter. [Adapter handoff](docs/adapter_handoff_prompt.md)

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

The archived LightRAG stores require the matching pre-HippoRAG source and
runtime recorded in their manifests. The current code requires fresh snapshots.

## HippoRAG 2

- Official SDK `2.0.0a5`, commit `d5c8329422e0a0b834a15874545cb6a74b4f9b26`.
  The Windows worker was verified with Python 3.12.1, NumPy 1.26.4 and
  PyArrow 22.0.0. `--arch hipporag2` selects native `index()` and `retrieve()`
  via a separate worker. [Windows dependency lock](requirements-locks/hipporag2-windows.txt)
- The fixture and Groq profiles use native retrieval top-k 40, fact linking
  top-k 5, one OpenIE worker and a 3,072-token shared evidence budget. Native
  scores, source metadata and graph seeds are captured. Retrieved graph
  paths and path lengths are unavailable from the result API. Proof
  availability is scored independently of invalid output.
- The guarded Groq callback passed an offline mock transport check for token
  limits and HTTP 429 capture. The first live preflight used
  `openai/gpt-oss-20b` on one synthetic denial from the stratified pilot
  subset. Native OpenIE's two calls settled at $0.00014385 under the shared
  $2 policy and preserved the explicit denial with both entity IDs in one
  extracted triple. The model also returned additional triples about the
  registry wording. Raw captures are in `runs/groq-provider-control-v1/`
  and the extraction record is in
  `runs/hipporag2-live-smoke-20261124/preflight/openie.json`.
- The local BGE cache is ready at revision
  `aa8f8b060edb00e03bfdd08813a2949946c8ba55`. All five ModelScope mirror
  files matched the saved LightRAG SHA-256 checksums, and FastEmbed produced
  a 384-dimensional vector offline. The initial two extraction calls are
  the recorded live HippoRAG 2 preflight. [LightRAG snapshot manifest](indexed_graphs/groq-pilot/conflict/snapshot_manifest.json)
- Run `scripts/run_groq_pilot.py --arch hipporag2 --key-slot 1 --dry-run`
  with the HippoRAG environment to inspect the live plan. The default plan
  uses 10-document checkpoints, 30-second indexing and 60-second scoring
  intervals, the shared ledger, the frozen pilot and shared prompt, and
  a 3,072-token budget. The single-key option retains ledger pacing and
  uses the first configured credential. [HippoRAG 2 Groq commands](docs/hipporag2.md#groq-configuration)
- The authorized full Groq pilot started on 24 November 2026 using
  `scripts/run_groq_pilot.py --arch hipporag2 --key-slot 1 --output-root runs/hipporag2-groq-pilot`
  under the shared $2 cap and default pacing. The conflict index completed
  with 120 of 120 documents and verified native file checksums. Conflict
  scoring reached 16 of 24 cases before Groq returned HTTP 429 on its
  daily token quota. The guarded ledger verified the failed request and
  retained its reservation and response. The experiment resumes with the
  same case order, indexes, model, prompt and budget after quota refill.
  Groq returned a 302-second Retry-After. After that interval elapsed, the
  user requested a second credential. A guarded key-slot-2 probe returned
  HTTP 200 with 999 daily requests remaining, and the runner resumed from
  the existing index and 16 completed cases under the same shared ledger.
  Checkpoints and raw traces are in `runs/hipporag2-groq-pilot/`.

The pilot finished all 48 cases on 25 November 2026. Both independent
120-document indexes and both scored runs passed checksum verification.
Slot 2 finished conflict scoring and eight control cases before a second
captured HTTP 429. Slot 3 resumed after the recorded 308-second Retry-After
and completed control scoring. A process interruption at 13 control cases
left one reserved request. The ledger retained the reservation. We verified
the old process had exited, archived its lock and resumed with both original
indexes and completed case checkpoints. At completion the shared ledger
verified $0.060481050 charged, including earlier probes, and $0.005432400
held for two captured 429s and the interrupted reservation.

| Hops | Conflicts detected | Missed | Invalid conflicts | Full proof delivered | Exact proof citations | Control false alarms | Invalid controls |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5/8 | 2/8 | 1/8 | 6/8 | 1/8 | 1/8 | 1/8 |
| 2 | 2/8 | 6/8 | 0/8 | 2/8 | 1/8 | 1/8 | 0/8 |
| 3 | 0/8 | 7/8 | 1/8 | 1/8 | 0/8 | 2/8 | 0/8 |

Complete-proof metrics apply to conflict cases. The live pilot is provisional
and has `benchmark_eligible=false`.
[Verified live per-hop report](results/hipporag2-groq-pilot-20261125/results_by_hop.json)

The latest frozen 48-case fixture recheck built two separate 120-document
indexes. All 48 responses parsed and all 1,824 delivered passage instances
mapped to exact source text. The maximum delivered envelope was 3,041 tokens.
The run is marked `benchmark_eligible=false`.

| Hops | Conflicts detected | Full proof delivered | Exact role-aware citations | False alarms | Invalid answers |
|---|---:|---:|---:|---:|---:|
| 1 | 5/8 | 5/8 | 5/8 | 0/8 controls | 0/16 |
| 2 | 2/8 | 2/8 | 2/8 | 0/8 controls | 0/16 |
| 3 | 2/8 | 2/8 | 2/8 | 0/8 controls | 0/16 |

One two-hop case gained a complete delivered proof on the fresh build.
The earlier fixture run remains under `runs/hipporag2-fixture-20261124-v2/`
and the recheck indexes, traces, responses and scores are under
`runs/hipporag2-fixture-recheck-20261124/`. Earlier failed Parquet builds
remain in `runs/hipporag2-fixture-20261124/`.

The integration suite passed all 28 tests, including both native SDK checks,
fixture index and run reuse, and the one-key Groq pacing transport check.
The earlier 30-document build completed from a 15-document checkpoint.
Ruff passed. The unit suite passed 94 tests and had one Windows symlink
privilege error (`WinError 1314`). The live Groq profile loaded the verified
BGE model locally.

[HippoRAG 2 setup](docs/hipporag2.md) · [Latest per-hop report](results/hipporag2-fixture-recheck-20261124/results_by_hop.json) · [Earlier fixture verification](results/hipporag2-fixture-20261124/verification.json)

## PathRAG

The worker pins the upstream BUPT-GAMMA/PathRAG commit
`32567bfc93605b8393996d5fa9ccdc0edbb865b2` and uses native `ainsert` and
hybrid context-only `aquery`. Its model callbacks use the shared Groq
GPT-OSS 20B provider and 384-dimensional local BGE for the live profile.
The final prompt and 3,072-token budget match the LightRAG comparison.
The pinned Windows environment passed installation and `pip check`.
[PathRAG setup and run commands](docs/pathrag.md)

The full 48-case native fixture run built two separate 120-document indexes,
resumed both builds from 60-document checkpoints and reused both scored
runs. All 48 answers parsed. All 1,824 delivered passage instances mapped
to exact source text, and the maximum delivered envelope was 3,071 tokens.
These fixture results have `benchmark_eligible=false`.

| Hops | Conflicts detected | Full proof delivered | Exact role-aware citations | False alarms | Invalid answers |
|---|---:|---:|---:|---:|---:|
| 1 | 0/8 | 0/8 | 0/8 | 0/8 controls | 0/16 |
| 2 | 1/8 | 1/8 | 1/8 | 0/8 controls | 0/16 |
| 3 | 0/8 | 0/8 | 0/8 | 0/8 controls | 0/16 |

The fixture indexes and complete case traces are under
`runs/pathrag-fixture-20261125/`. The native worker saves the raw context
and attributes returned source text to neutral paths through the native
chunk store. Scores, directed paths, path lengths and graph-row source IDs
are unavailable in the native context response.
[PathRAG fixture report](results/pathrag-fixture-20261125/results_by_hop.json)

The native opt-in test passed with both conditions, a 15-document build
checkpoint and reuse of both completed indexes and scored runs. Ruff passed.
The unit suite passed 94 tests and hit the existing Windows symlink privilege
error. The local BGE callback produced a 384-dimensional embedding from the
baseline's checksum-verified weights.
All 29 integration tests passed in the environment with the optional
provider packages installed. The saved LightRAG report and both native
snapshot checksums remain available. A restore attempt with the current
checkout failed the original source and runtime checks. The saved snapshots
record Python 3.12.13, while the local LightRAG worker uses 3.12.1.

The authorized live run started after HippoRAG 2 finished. It uses
`scripts/run_groq_pilot.py --arch pathrag --key-slot 3 --rotate-on-quota`.
The runner keeps the shared $2 cap, uses 10-document batches, and paces
requests at 30 seconds during indexing and 60 seconds during scoring.
After a captured HTTP 429 and its Retry-After, it advances to the next
configured slot and wraps after the last. Live checkpoints and case traces
are under `runs/pathrag-groq-pilot/`. The first live checkpoint passed
checksum verification with 10 conflict documents, 22 graph vertices and
12 edges after 10 audited Groq calls. The resumed build checkpointed 60
conflict documents under the same index identity. Key slot 3 then hit a
daily token limit and the ledger verified the HTTP 429. The runner honored
its 505-second Retry-After, advanced to slot 4 and resumed from the
60-document checkpoint. The conflict index completed all 120 documents
with 141 graph vertices and 117 edges and passed checksum verification.
Slot 4 reached 19 of 24 conflict cases before its own daily token limit.
The runner honored the captured 195-second Retry-After, switched to slot 5
and reused the completed conflict index and case checkpoints. All 24
conflict cases are now checksum-verified. Slot 5 completed the separate
120-document control index with 161 graph vertices and 113 edges. Both
native indexes passed checksum verification and have distinct identities.
Control scoring checkpointed one case before a DNS connection error. The
shared ledger verified the captured failure and retained its reservation.
The runner resumed with slot 5 and the existing checkpoints. Slot 5 reached
15 control cases before its daily token limit. The runner honored the
763-second Retry-After and switched to slot 6. Slot 6 completed all remaining
controls on 25 November 2026.

| Hops | Conflicts detected | Missed | Invalid conflicts | Full proof delivered | Exact proof citations | Control false alarms | Invalid controls |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0/8 | 7/8 | 1/8 | 1/8 | 0/8 | 0/8 | 0/8 |
| 2 | 0/8 | 8/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 |
| 3 | 0/8 | 8/8 | 0/8 | 0/8 | 0/8 | 0/8 | 0/8 |

All 48 native retrievals returned evidence, and all 1,824 delivered
passage instances mapped to exact source text. The maximum envelope was
3,070 tokens. Both scored runs passed checksum verification. The verified
report matches the HippoRAG 2 pilot's frozen dataset and prompt hashes,
model, embedding model and evidence budget. These live scores are
provisional and have `benchmark_eligible=false`. At completion, the
shared ledger verified cumulative charges of $0.154451775 and reservations
of $0.013801425 under the $2 cap. That ledger includes prior experiments
and key checks.
[Verified live per-hop report](results/pathrag-groq-pilot-20261125/results_by_hop.json)

## Current scope and shared updates

The original delivery covered LightRAG through Step 4. HippoRAG 2 and
PathRAG are implemented, and both live pilots are complete.
Microsoft GraphRAG Local Search is pending.
Each implementation should expose its native capabilities and
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
