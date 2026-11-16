# Protocol implemented through Step 4

The benchmark is an artificial documentary world. Each family selects one
declared transitive predicate and a directed positive chain of 1–3 assertions.
A positive case denies the chain's conclusion. A matched control denies a
relationship to another entity for which there is no positive proof. Absence
does not imply negation. Each edge has a distinct source assertion document.
Two unrelated positive documents serve as close-topic distractors.

CONTAINED_IN applies to physical_entity, SUBREGION_OF to region, and PRECEDES to
event. The current ontology makes all three transitive and irreflexive. These
rules apply only inside the synthetic world. They do not license compositions
for arbitrary real-world predicates.

All simple directed positive paths are searched. The reasoner retains all
shortest proofs, rejects positive cycles/type errors and intersects proof/denial
validity intervals. Certificates bind the graph, ontology, derived conclusion,
shortest edge sets and opposing assertion. Generated corpus intervals are open
ended; finite/disjoint intervals are covered by independent fixtures.

The same query is used in both conditions. IDs and source prose do not expose
condition labels or chain positions. Native indexing receives only document
bytes and neutral IDs. Pilot conditions have distinct native index snapshots.
For a future full set, families are split approximately 20/20/60 into design,
development and test. The pilot is separate and is not a held-out evaluation.

The adapter uses the upstream ingestion and retrieval APIs, captures structured
native data before final generation, and saves that raw response. It builds a
stable envelope from chunks and native entities/relations/references without
adding canonical conclusions. Budgeting retains source chunks in native order,
then includes graph rows that fit. Any omissions are logged. The exact delivered
JSON envelope is measured with cl100k_base, separately from native retrieval's
max_total_tokens. Native relative chunk scores are unavailable and remain null.
Path length is unobservable in this adapter and remains null.

Gold source-to-edge alignment happens outside the model prompt. Only a complete
asserted source sentence, matched against the attributed document and delivered
verbatim, receives a mapped assertion ID. A graph description or source ID alone
is insufficient. Complete-proof retrieval in the current scorer covers verbatim
source chunks; possible proof content in native summaries is not credited.

A small P1-style generation seam asks for JSON source quotes, stores raw output,
validates strictly and aligns citations deterministically. The scorer separates
detection TP/TN/FP/FN, exact witness matching and retrieval completeness. It does
not implement the later official statistical evaluation. Invalid JSON has an
explicit error count and lowers valid_output_rate; metric names with valid_rows
exclude errors and must not be read as unconditional official performance.

The final prompt uses the same generic rulebook in all conditions. The fixture
answer model independently searches only delivered statement text, and receives
neither labels nor canonical proofs. It is a test double, not an LLM baseline.

