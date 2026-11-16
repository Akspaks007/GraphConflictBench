# GraphConflictBench benchmark readiness

Prepared 15 November 2026, Asia/Kolkata. Scope: review and preparation of the completed Step 4 implementation. No paid requests, label edits, additional architectures or Step 5 implementation were performed.

**Decision: ready for human review; not yet ready for an approved real-provider run or research performance claims.** Logical labels and source provenance pass, but model-visible build timestamps provide an unintended condition proxy. Spending enforcement, live-provider extraction fidelity and human signoff remain unresolved.

## Deliverables

| File | Purpose |
| --- | --- |
| [case_review.html](case_review.html) | Searchable, expandable report of all 48 cases; fully offline |
| [case_review.md](case_review.md) | Full readable question, documents, expected label, denial, source spans and every shortest proof for each case |
| [case_review.json](case_review.json) | Structured per-case findings, missing witness IDs and review flags |
| [human_review.csv](human_review.csv) | 48-row worksheet; reviewer fields deliberately blank |
| [audit_findings.json](audit_findings.json) | Machine-readable logical, provenance, leakage and fidelity checks and cost assumptions |
| [real-smoke.proposed.yaml](real-smoke.proposed.yaml) | Valid configuration proposal; never executed against a provider |
| [smoke_commands.md](smoke_commands.md) | Exact existing CLI commands, prerequisites and fresh output paths |
| [smoke-dataset/dataset_manifest.json](smoke-dataset/dataset_manifest.json) | Separately generated, automatically audited 12-case smoke input |
| [build_review.py](build_review.py) | Offline report builder; no inference calls |

The review artifacts contain gold labels, canonical assertions and proof certificates. They are human-only materials. Only the smoke dataset's `corpora/pilot/{condition}/documents.jsonl` exports may cross the native indexing boundary. Do not index this folder, the review reports or the dataset's gold JSONL files.

## Verification performed

The existing validator was rerun on the pilot and the new smoke dataset. In addition, an independent breadth-first implementation verified each pilot's positive shortest paths and the presence/absence of a positive path to its denied object. This independent check applies to the timeless, three-transitive-predicate pilot; finite-interval semantics remain covered by the existing reasoner and logical fixtures.

| Check | Observed result |
| --- | --- |
| Original artifact integrity | 739/739 original SHA256 hashes unchanged |
| Pilot counts | 48 cases, 24 paired families, 144 source documents, 192 entities |
| Independent label/path checks | 48/48 agree with certificates and gold labels |
| Depth/condition balance | Eight cases in each of the six depth × condition cells |
| Pair checks | 24/24 have identical questions, depth, predicate and split; denial subject/predicate/polarity/intervals match and only its object changes |
| Condition isolation | 96 shared documents; 24 conflict-only and 24 control-only documents; separate native indexes |
| Saved index and run manifests | All recorded checksums verified |
| Original native full documents and chunks | 120/120 verbatim documents and 120/120 verbatim chunks per condition |
| Saved model prompts | 48/48 rebuilt exactly from source, captured evidence and the shared prompt |
| Direct gold injection | No forbidden gold fields, canonical assertion IDs or wrong-condition document IDs found in the 48 saved final model payloads |
| Indirect metadata leakage | **Found: all 48 prompts expose condition-correlated build timestamps** |
| Human validation | Pending; not inferred from automatic checks |
| Trained leakage classifier | Not run |

The previously verified 43-test result is in `../recheck-20261115-windows/verification.json`. Current task check results are recorded in `validation.json`; no native adapter code was changed.

## Main blocker: timestamps reveal build condition

`prompts.evidence_envelope()` includes `retrieval.native_graph` as supplied. Its retained entity rows include `created_at`, an ingestion timestamp rather than a fact in the fictional documentary world.

| Saved condition | Smallest timestamp | Largest timestamp | Delivered timestamp-bearing rows |
| --- | --- | --- | --- |
| Conflict | 1794685336 | 1794685341 | 227 |
| Control | 1794685394 | 1794685399 | 328 |

All 48 cases have such timestamps in their model-visible payloads. A threshold between these nonoverlapping ranges separates the saved conditions in-sample. This is a concrete metadata proxy, not a trained/generalizing classifier result or evidence that a model actually used it. Sequential condition builds could recreate the confound in a real-provider run.

**Recommended remediation, not implemented:** retain complete native rows in raw traces; define a reviewed allowlist for the model-visible graph envelope that excludes volatile build metadata such as `created_at`. Verify polarity, provenance and evidence-token accounting after that change. Any implementation/prompt/config change requires fresh snapshot/run paths and the native integration test under AGENTS.md. Do not edit historical prompts or evidence, and do not modify the gold labels.

The raw input texts, neutral IDs, generic relation rules and response schema show no direct label injection. Generic uses of the word “conflict” in the shared question/instructions are not condition labels. Opaque IDs are not a proof of blindness: these are published deterministic pilot artifacts, and a lookup table could memorize them. Review materials must be withheld from evaluation models.

## Extraction and evidence fidelity

The saved native fixture snapshots contain exactly the expected condition documents. Every one of the 240 document instances and source chunks matches its original text, with a valid document path and full assertion sentence. All 120 assertions per condition are also found verbatim in source-attributed native relationship descriptions. This is a new offline audit of fixture extraction artifacts, not a real-model extraction experiment.

Native graph structure is undirected. The conflict graph has 144 nodes/112 edges and the control graph 168 nodes/120 edges. Eight depth-1 conflicts merge a positive assertion and its explicit denial onto the same endpoint pair. Both sentences survive in descriptions, but native adjacency alone cannot distinguish their polarity or direction. Keyword predicates also do not encode polarity separately. Review the actual negative wording, never infer a directed proof from native endpoint order. Fixture entity types are `other`, not an independently recovered copy of the canonical typed ontology.

Across the 48 saved pilot queries, 1,734 raw source-chunk occurrences were delivered and all 1,734 have exact source-backed assertion mappings. None were removed by the evidence envelope. All 48 envelopes did omit graph rows to meet the 4,096-token limit. They retained 555 entity rows and 66 references in total, but **zero relationship rows**. Thus these delivered contexts contain source statements and some native entity metadata; they do not expose retrieved relation paths. Raw relationship rows remain available in the per-case native response traces.

The nine missing-proof cases already lacked the required assertions in the raw retrieved chunks. The missing assertion sentences were also absent from their raw retrieved relationship descriptions. These misses were not caused by the final envelope dropping source chunks. This does not establish the underlying retrieval mechanism or generalize beyond the fixture run.

Evidence mapping is intentionally conservative: it requires one neutral source filename, exact text containment and the complete canonical assertion sentence. Aggregated/absolute/unrecognized paths, paraphrases and graph summaries can remain unmapped. That favors precision over recall. Current short documents occupy one chunk; a future multi-chunk document would encounter the citation aligner's last-chunk-per-document lookup, so that broader case is unverified.

Live-provider fidelity remains unknown. In particular, extraction must preserve negation, opaque entity names, source attribution and both contradictory claims rather than “repairing” them. With native extraction caching disabled, `models.py` does not separately persist each raw extraction/gleaning provider reply or full failed transport response. Successful native build usage and parsed stores are saved; final generation text and parse failures are retained when the call returns. This is insufficient for a complete raw extraction-response audit. A provider gateway or separately approved logging change would be needed to retain complete request/response/error records without changing retrieval semantics.

## Case-specific attention

No incorrect gold label, invalid shortest path or ambiguous source-to-assertion span was found by the automatic checks. All 48 cases still need human signoff and review of the timestamp proxy.

| Group | Count | Human attention |
| --- | --- | --- |
| All cases | 48 | Fictional rules, opaque names, question scope, exact source wording, timestamp proxy and pending signoff |
| Controls | 24 | Hop depth describes a separate supporting chain; there is no positive proof to the alternative denied object. Do not infer negative truth from absence. |
| Depth-1 conflicts | 8 | Positive and negative sentences share one undirected native edge; check both source claims survive. |
| Historical fixture proof-retrieval misses | 9 | Review exact missing assertions and paired controls; do not change labels, depth or retrieval settings to accommodate responses. |

Priority retrieval cases, all in the conflict condition:

| Case | Family | Depth | Predicate | Missing witness assertions |
| --- | --- | --- | --- | --- |
| Ca5cf3e75e3d2fddf1810 | F20006 | 2 | CONTAINED_IN | E0fd0a1d330b69a1064cf |
| Cd4415c7ca842d8437c46 | F20007 | 2 | SUBREGION_OF | Ead7f5f4ff1e53f40bdf0 |
| C9ad27ae96d1771959b51 | F30000 | 3 | CONTAINED_IN | E60ac2b434d56c4db1105; Ea46ceeb6284181742429 |
| C18c3b347fd4b60f07d70 | F30001 | 3 | SUBREGION_OF | E570c5a8715a0c2da81da; Edb8e57de3f5ac8e94f65 |
| C588987f4cc3505b4717d | F30003 | 3 | CONTAINED_IN | Ec471bdd989cd33fcd65a |
| Cd232869ea3c6d7941431 | F30004 | 3 | SUBREGION_OF | E123f6c8c8971a755674c; E535bc9abc1e5ada65190 |
| C904e17d3e62812902b13 | F30005 | 3 | PRECEDES | E0864612b7ebf232487a2 |
| C2d191d934a58992b6ebe | F30006 | 3 | CONTAINED_IN | E330fa9dc40c41686788a; E45724dd9a7ae4e83665f |
| C42ca936fcf6590680a3a | F30007 | 3 | SUBREGION_OF | E324bf33ddca21961b184; E47fd7dcfe5a75a3307e6 |

Each case's report includes its paired case ID, verbatim family documents, explicit denial, ordered shortest path(s), gold witness sets, saved fixture outcome, and assertions missing before and after budgeting. Relevant family documents are shown for readability; actual native retrieval searched all 120 documents for the condition.

## Scoring and interpretation limits

An offline probe on case `C3e26105ec36803f12b2e` swapped the saved prediction's support/opposing citation lists in memory. The response remains schema-valid and `exact_proof_set` remains true, because the scorer compares the union of mapped assertion IDs. No saved prediction was changed. The metric does not establish correct citation roles, explanation fidelity, or attribution of every individual conflict object. Manual role review is required for the smoke; formal localization claims need a separately reviewed scorer improvement. Do not silently relabel or rescore historical evidence.

A negative answer with `evidence_status=insufficient` does not establish that the full corpus has no conflict. The small scorer reports detection, source-chunk proof completeness and localization separately; invalid-output denominators and raw failures must stay visible. Fixture success and its 15 TP/9 FN/24 TN pilot tally are plumbing observations, not LLM/LightRAG benchmark findings.

## Human-review checklist

- [ ] Reviewer and date recorded for every case; leave no item implicitly approved.
- [ ] Fictional ontology is explicit: transitivity is licensed only for the three declared predicates; no real-world containment assumption overrides it.
- [ ] Each document asserts exactly the recorded subject/predicate/object/polarity and source span.
- [ ] Every displayed path is directed, shortest and composed of distinct source assertions; the denial is separate from supporting hop count.
- [ ] The denial matches the supported conclusion for conflicts; controls deny a different object without a positive proof to it.
- [ ] Paired questions, positive documents and distractors match; only the denied object changes.
- [ ] Opposite-condition denial documents never enter the index or model payload.
- [ ] Direct gold fields and human-review artifacts are absent from all model inputs; build metadata proxies are resolved before live evaluation.
- [ ] Source quotes, negation, source IDs and both depth-1 claims survive native extraction; no source truth is chosen by extraction.
- [ ] Retrieval misses, unmapped evidence and omitted graph rows are recorded; missing evidence does not justify changing labels.
- [ ] Support and opposing citation roles, exact quotations and explanation relevance are checked manually.
- [ ] A decision of accept / question / reject with a rationale is entered in `human_review.csv`; disputed cases are escalated without editing the generated snapshot.
- [ ] A second reviewer adjudicates questions/rejections and checks all nine priority misses and eight merged-edge conflicts.

## Proposed 12-case real-provider smoke

The prepared input is `smoke-dataset/`: six families, 12 paired cases, 36 unique documents, 30 documents per condition. It was generated with the existing CLI, seed 42, and passes the existing audit. All 12 case IDs overlap the pilot; this is a plumbing/format/fidelity check, not held-out evaluation.

**Coverage limitation:** existing `generate --size smoke` has two families per depth and always chooses only CONTAINED_IN and SUBREGION_OF (six cases each). PRECEDES is absent. `run --limit 6` on the 48-case pilot would instead select the first six cases per condition, all depth 1, while still indexing 120 documents; do not confuse that with this smoke. Accept the narrow plumbing coverage explicitly, or approve preparation of a separate stratified smoke dataset. The pilot is unchanged.

Proposed configuration keeps native hybrid retrieval and the existing token budgets, chunking, embedding dimension and one gleaning pass. It pins `gpt-4o-mini-2024-07-18`, uses `text-embedding-3-small` at 1536 dimensions, reduces concurrency to 1 and SDK retries to 0, and sets `benchmark_eligible=false`. `run` still labels provider output `provisional_pilot`; the false eligibility flag excludes this readiness exercise from research results.

The existing provider wrapper uses the same LLM for extraction, gleaning, keywords, summaries and final generation; independent role-model choices are not supported. Sampling temperature is fixed at 0. Provider response-format kwargs supplied by native keyword extraction are currently ignored unless the wrapper receives its separate `keyword_extraction` flag. Final JSON relies on the shared prompt plus strict parsing, not provider-enforced JSON Schema. Native keyword parsing may normalize/repair its own JSON; final benchmark predictions are not repaired.

Model choice needs approval. The official [GPT-4o mini model page](https://developers.openai.com/api/docs/models/gpt-4o-mini) marks the model deprecated. The [deprecation schedule](https://developers.openai.com/api/docs/deprecations) lists a January 14, 2027 shutdown and recommends GPT-6 Luna. The proposal pins the existing compatible model for an immediate smoke rather than silently migrating the provider contract. Access has not been checked with a live account. If the smoke occurs after shutdown or that model is unavailable, stop and review a replacement, its API parameter compatibility and pricing; do not silently fall back.

The `.venv` core environment lacks `openai` and `numpy`, so the README's core-interpreter real `run` would fail at final generation. Both dependencies are already installed at locked versions in `.venv-lightrag`. The proposed commands run the existing CLI under that environment and retain the native subprocess boundary with the same worker interpreter. This changes no source files or dependencies. If strict separate core/native package sets are required for the live run, approve installing the locked model dependencies into core and record its new freeze instead.

## Expected API usage and cost

Prices checked against official pages on 15 November 2026. Standard online USD token rates; no Batch/caching discount, taxes, foreign exchange or gateway fees included. The proposed GPT-4o mini uses $0.15/M input and $0.60/M output tokens ([model pricing](https://developers.openai.com/api/docs/models/gpt-4o-mini)); text-embedding-3-small uses $0.02/M tokens ([embedding pricing](https://developers.openai.com/api/docs/models/text-embedding-3-small)).

| Stage | Expected successful LLM calls | Input tokens | Assumed output tokens | Estimated USD |
| --- | --- | --- | --- | --- |
| Initial document extraction | 60 | 109,076 | 18,000 | 0.0271614 |
| One gleaning pass | 60 | 151,376 | 6,000 | 0.0263064 |
| Entity/relation summaries allowance | 0–12; budget 12 | 24,000 | 4,800 | 0.0064800 |
| Retrieval keyword extraction | 12 | 8,244 | 1,800 | 0.0023166 |
| Final JSON generation | 12 | 66,000 | 9,600 | 0.0156600 |
| Embeddings: documents, entities, relationships and queries | Batched; not one request per document | 50,000 embedding-token allowance | — | 0.0010000 |
| **Central estimate** | **144–156 LLM calls** | | | **0.0789244** |

The cost builder reconstructs the installed native extraction and keyword templates without calling an LLM. Initial extraction input is approximately 1,813–1,824 cl100k_base tokens per document including estimated message overhead. Source texts across both smoke corpora contain only 3,416 cl100k_base tokens; most extraction input cost comes from repeated instructions. Gleaning includes initial history and an assumed 300-token extraction response. Actual billing tokenizer totals can differ.

The 60 document instances should each produce one chunk. One gleaning pass follows each extraction when allowed by the native input guard. Summary calls are data-dependent; normal short descriptions may require none, but 12 are budgeted. Rebuilding both conditions intentionally pays again for shared documents. Query retrieval can embed keywords and source/vector queries; the embedding allowance covers source, entity and relation text plus query-time requests and incremental upserts. Expect roughly 200–400 embedding input records, but HTTP batch/request counts and description lengths depend on live extraction and cannot be promised from fixture data.

Use a planning range of **$0.05–$0.30**, with no claim that it is a guaranteed bound. A stress allowance of 2M LLM input, 250k output and 200k embedding tokens costs about **$0.454** at these rates. All estimates exclude charges from retries/failures whose billing is unknown. Concurrency and SDK retries are reduced, but upstream orchestration/failure recovery and manual reruns are additional uncertainty. Do not automatically retry the complete smoke after a failure.

### Proposed hard cap: USD 2.00, not yet enforced

The existing CLI has **no** `--max-cost`, global token ledger, or per-role completion-budget setting. `max_total_tokens`/`evidence_budget` constrain retrieval context, not total paid API usage. The wrapper does not send an LLM completion cap. Adding unsupported budget keys to YAML would fail the strict adapter schema.

Use a dedicated project/key and enable an enforced project spend limit as a backstop. Current official [project guidance](https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform) says an enforced limit stops requests after tracked spending reaches it, but enforcement can lag and exceed the configured amount slightly. An alert without enforcement does not stop requests. Therefore a dashboard limit alone is not an exact $2.00 hard ceiling.

For a strict cap, approval should require a compatible billing gateway or a separately approved application guard that reserves worst-case request cost **before dispatch**, atomically across native workers and final generation. It must include embedding calls, maximum completion tokens, failures/retries and in-flight reservations, and retain unknown failed usage conservatively. It must log raw request/response/error records and route both subprocess and final generation through the same ledger. A proposed gateway can use `OPENAI_BASE_URL`; none is configured or implemented here. Reservation + settled usage must never exceed $2.00. Recommend an operator pause/reconciliation at $0.50 and at each condition boundary. No changes to account limits were made.

## Blockers and approval decisions

| Item | Status / consequence |
| --- | --- |
| Timestamp condition proxy | Block benchmark-ready live prompts until reviewed removal from the model-visible envelope; preserve raw evidence |
| Human review | All 48 pending; at least the smoke's 12 cases and their pair semantics must be signed off before paid smoke |
| Strict $2.00 enforcement | Not provided by existing code; an enforcement mechanism must be approved and verified |
| Raw live extraction/failed-response capture | Incomplete with current wrapper; approve gateway capture or a focused logging change for full fidelity audit |
| Model availability/deprecation | Approve pinned legacy model for immediate compatibility smoke, or review a replacement; no silent substitution |
| Live-provider route | Implemented but unexecuted; access, formatting rate, negation preservation and usage remain unknown |
| Smoke predicate coverage | No PRECEDES; approve limited plumbing scope or a different fresh input set |
| Citation-role scoring | Manual role audit required; blocks strong automatic localization claims, not an explicitly limited plumbing check |
| Core model dependencies | Use the installed native environment for orchestration as documented, or approve core model dependency installation |

No blocker was “fixed” by changing source assertions, labels, proof depth, historical responses or snapshot evidence. The next concrete work to approve is a focused Step 4 model-input metadata filter plus capture/spend-enforcement preparation, followed by fresh native fixture verification. Paid execution remains a separate approval after human review and the above decisions.
