# Pilot case review — human reviewers only

48 cases / 24 paired families. Generated 15 November 2026. This artifact contains gold labels and canonical witnesses: never index it or add it to generation prompts. Automated logical verification is complete; human approval is pending. All original texts are reproduced verbatim. Readiness is blocked by the model-visible build timestamp condition proxy described in benchmark_readiness.md.

Each case lists only its relevant family documents. Actual native retrieval searches the full 120-document condition corpus, including other families. Edge-role annotations and shortest paths below are reviewer-only.

For controls, hop depth labels the separate positive chain to the canonical target. There is no positive proof to the explicitly denied alternative object. No conflict demonstrated is an open-world conclusion, not a declaration that the denial or any source is true.

## Case index

| Case | Pair family | Condition | Depth | Predicate | Saved fixture outcome | Attention |
| --- | --- | --- | --- | --- | --- | --- |
| [C3e26105ec36803f12b2e](#c3e26105ec36803f12b2e) | F10000 | conflict | 1 | CONTAINED_IN | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [C96e62542ee1b2f486b9f](#c96e62542ee1b2f486b9f) | F10000 | control | 1 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C42bbd4765e6d5519d2b2](#c42bbd4765e6d5519d2b2) | F10001 | conflict | 1 | SUBREGION_OF | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [C221076261f1c382e4bda](#c221076261f1c382e4bda) | F10001 | control | 1 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cdfdb9e95adde8d038e30](#cdfdb9e95adde8d038e30) | F10002 | conflict | 1 | PRECEDES | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [C9ff35c7464e3e294054b](#c9ff35c7464e3e294054b) | F10002 | control | 1 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cec8bb9e3d570ee94ba8e](#cec8bb9e3d570ee94ba8e) | F10003 | conflict | 1 | CONTAINED_IN | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [Cbe622777f555a0d79985](#cbe622777f555a0d79985) | F10003 | control | 1 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C45be00a9a7ad99b996ad](#c45be00a9a7ad99b996ad) | F10004 | conflict | 1 | SUBREGION_OF | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [Cb5f1498885e5977e31a0](#cb5f1498885e5977e31a0) | F10004 | control | 1 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Ceb082b2014ab0733ca7c](#ceb082b2014ab0733ca7c) | F10005 | conflict | 1 | PRECEDES | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [C9d23b5521dfd594f827d](#c9d23b5521dfd594f827d) | F10005 | control | 1 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cdfa0fc2ed7b9fb7e49cb](#cdfa0fc2ed7b9fb7e49cb) | F10006 | conflict | 1 | CONTAINED_IN | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [C05c58bea507790542472](#c05c58bea507790542472) | F10006 | control | 1 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cdb61bd674a8718cdab06](#cdb61bd674a8718cdab06) | F10007 | conflict | 1 | SUBREGION_OF | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge |
| [Ce9e17b943ef1908e97e1](#ce9e17b943ef1908e97e1) | F10007 | control | 1 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C7e7d62477508e2b4388a](#c7e7d62477508e2b4388a) | F20000 | conflict | 2 | CONTAINED_IN | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [C4bd4688564a242ecf137](#c4bd4688564a242ecf137) | F20000 | control | 2 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C7ea8d2cba383bd89ac9d](#c7ea8d2cba383bd89ac9d) | F20001 | conflict | 2 | SUBREGION_OF | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [C5ef6d9ade86682fff037](#c5ef6d9ade86682fff037) | F20001 | control | 2 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C284858966dec17b70c96](#c284858966dec17b70c96) | F20002 | conflict | 2 | PRECEDES | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [C85bfbe12307f7f880a90](#c85bfbe12307f7f880a90) | F20002 | control | 2 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C8df4eb422ddda77c47ec](#c8df4eb422ddda77c47ec) | F20003 | conflict | 2 | CONTAINED_IN | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [C6522cdd91136ea81cb55](#c6522cdd91136ea81cb55) | F20003 | control | 2 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C4a7e4f1a97759d4e6cc0](#c4a7e4f1a97759d4e6cc0) | F20004 | conflict | 2 | SUBREGION_OF | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [Cd65cb6bb1011932cfaaf](#cd65cb6bb1011932cfaaf) | F20004 | control | 2 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C7ea35110eeccbbdc7dc9](#c7ea35110eeccbbdc7dc9) | F20005 | conflict | 2 | PRECEDES | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [Cfa96317b5e41255c0ec2](#cfa96317b5e41255c0ec2) | F20005 | control | 2 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Ca5cf3e75e3d2fddf1810](#ca5cf3e75e3d2fddf1810) | F20006 | conflict | 2 | CONTAINED_IN | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [Cce7e332b5c6ca12c3659](#cce7e332b5c6ca12c3659) | F20006 | control | 2 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cd4415c7ca842d8437c46](#cd4415c7ca842d8437c46) | F20007 | conflict | 2 | SUBREGION_OF | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C4f22a075bbaa8c11d46e](#c4f22a075bbaa8c11d46e) | F20007 | control | 2 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C9ad27ae96d1771959b51](#c9ad27ae96d1771959b51) | F30000 | conflict | 3 | CONTAINED_IN | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C867476b9eda45605182a](#c867476b9eda45605182a) | F30000 | control | 3 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C18c3b347fd4b60f07d70](#c18c3b347fd4b60f07d70) | F30001 | conflict | 3 | SUBREGION_OF | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C72bd1b5ee97f58f77f35](#c72bd1b5ee97f58f77f35) | F30001 | control | 3 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C45e88caf1e8b13cac59e](#c45e88caf1e8b13cac59e) | F30002 | conflict | 3 | PRECEDES | tp | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy |
| [Ca13cd3fae860c8b5fd24](#ca13cd3fae860c8b5fd24) | F30002 | control | 3 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C588987f4cc3505b4717d](#c588987f4cc3505b4717d) | F30003 | conflict | 3 | CONTAINED_IN | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [Cda357462e04448e2e7f8](#cda357462e04448e2e7f8) | F30003 | control | 3 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [Cd232869ea3c6d7941431](#cd232869ea3c6d7941431) | F30004 | conflict | 3 | SUBREGION_OF | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C8b19850343875fd938d3](#c8b19850343875fd938d3) | F30004 | control | 3 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C904e17d3e62812902b13](#c904e17d3e62812902b13) | F30005 | conflict | 3 | PRECEDES | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C734bcf501f31be8fc084](#c734bcf501f31be8fc084) | F30005 | control | 3 | PRECEDES | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C2d191d934a58992b6ebe](#c2d191d934a58992b6ebe) | F30006 | conflict | 3 | CONTAINED_IN | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C292080bf6559fd1f67d3](#c292080bf6559fd1f67d3) | F30006 | control | 3 | CONTAINED_IN | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |
| [C42ca936fcf6590680a3a](#c42ca936fcf6590680a3a) | F30007 | conflict | 3 | SUBREGION_OF | fn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete |
| [C003f7fb031839821d2d0](#c003f7fb031839821d2d0) | F30007 | control | 3 | SUBREGION_OF | tn | human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain |

## C3e26105ec36803f12b2e

Pair: **F10000** / partner **C96e62542ee1b2f486b9f**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd3a7440e5b8f66ca8744? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ea51f6de09e12bc38988a` from `D8e1819f9a41f64977ff5`: `Nd3a7440e5b8f66ca8744 --NOT CONTAINED_IN--> N6401ff9770356cea0bdf`.

Canonical positive-chain target: `N6401ff9770356cea0bdf`. Denied object: `N6401ff9770356cea0bdf`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nd3a7440e5b8f66ca8744 --CONTAINED_IN [E75388636843585860838; D124fdca7dba8c4b80a96]--> N6401ff9770356cea0bdf
```

Conflict witness sets (support plus separate denial): `[["E75388636843585860838","Ea51f6de09e12bc38988a"]]`.

### Source documents (verbatim)

**D124fdca7dba8c4b80a96** — shortest-path support; assertion `E75388636843585860838`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `ce730cb23036a199cba3326300809870537510adc8ce5d892f8c088ff131be7d`.

> Nd3a7440e5b8f66ca8744 is contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D8e1819f9a41f64977ff5** — explicit denial; assertion `Ea51f6de09e12bc38988a`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `65f1a2a6dd24a7437c958fce36cab278fe9ca0759bd13d3befc65aef941e2cfa`.

> Nd3a7440e5b8f66ca8744 is not contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D567f46f31d8d3db00fc1** — unrelated distractor; assertion `E03130e5879a70edede9a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `18a0c20ae5666bd468a280309b956e99d3f7b52326b26feffd8279992fa09c7d`.

> N022fd25e2d10ef843baf is contained in Nf6af6bea55f905f52c6f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6cace2e54ebc61628653** — unrelated distractor; assertion `Eedbefdfe4a831de26ae8`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `dfb5e0450b87c69443be6fd20a3d799a8228edf499cd4adb8eb79ada74e2cd41`.

> N022fd25e2d10ef843baf is contained in N4cd9009c6402d4c37d26. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4088.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C96e62542ee1b2f486b9f

Pair: **F10000** / partner **C3e26105ec36803f12b2e**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd3a7440e5b8f66ca8744? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E3ebecb16ef5373787abd` from `Dfa1b226b2a08def00dc8`: `Nd3a7440e5b8f66ca8744 --NOT CONTAINED_IN--> N90b644b6fa099d0ec61b`.

Canonical positive-chain target: `N6401ff9770356cea0bdf`. Denied object: `N90b644b6fa099d0ec61b`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nd3a7440e5b8f66ca8744 --CONTAINED_IN [E75388636843585860838; D124fdca7dba8c4b80a96]--> N6401ff9770356cea0bdf
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D124fdca7dba8c4b80a96** — shortest-path support; assertion `E75388636843585860838`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `ce730cb23036a199cba3326300809870537510adc8ce5d892f8c088ff131be7d`.

> Nd3a7440e5b8f66ca8744 is contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfa1b226b2a08def00dc8** — explicit denial; assertion `E3ebecb16ef5373787abd`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `49889404ac7227547c1765687804c06a59edeaf54548884e345a1c159c8e3742`.

> Nd3a7440e5b8f66ca8744 is not contained in N90b644b6fa099d0ec61b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D567f46f31d8d3db00fc1** — unrelated distractor; assertion `E03130e5879a70edede9a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `18a0c20ae5666bd468a280309b956e99d3f7b52326b26feffd8279992fa09c7d`.

> N022fd25e2d10ef843baf is contained in Nf6af6bea55f905f52c6f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6cace2e54ebc61628653** — unrelated distractor; assertion `Eedbefdfe4a831de26ae8`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `dfb5e0450b87c69443be6fd20a3d799a8228edf499cd4adb8eb79ada74e2cd41`.

> N022fd25e2d10ef843baf is contained in N4cd9009c6402d4c37d26. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C42bbd4765e6d5519d2b2

Pair: **F10001** / partner **C221076261f1c382e4bda**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N4142a55c2d046b158499? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Edc35135bfb2f02dc716b` from `Dcf6378293bf1ac388f4e`: `N4142a55c2d046b158499 --NOT SUBREGION_OF--> Ne66dd9afcc8a121e916d`.

Canonical positive-chain target: `Ne66dd9afcc8a121e916d`. Denied object: `Ne66dd9afcc8a121e916d`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N4142a55c2d046b158499 --SUBREGION_OF [E3e90a150a45dd2fccc6d; D76413fefe6657c0277f5]--> Ne66dd9afcc8a121e916d
```

Conflict witness sets (support plus separate denial): `[["E3e90a150a45dd2fccc6d","Edc35135bfb2f02dc716b"]]`.

### Source documents (verbatim)

**D76413fefe6657c0277f5** — shortest-path support; assertion `E3e90a150a45dd2fccc6d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `bc271fd4000b30abddd0babfb6b73428b46eb189eefa9a807973c96041616d39`.

> N4142a55c2d046b158499 is a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcf6378293bf1ac388f4e** — explicit denial; assertion `Edc35135bfb2f02dc716b`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `45aadf8173e49c5c136bc6894e4a0d0accf3bc8951e5fab506354c0f564919e7`.

> N4142a55c2d046b158499 is not a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db8ef2d8f24e3cb70b9e7** — unrelated distractor; assertion `E08abfde37c7fce6d7036`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1c86873eb89cf1af9be18ffea32823ffc1a178ab074a474329e23d05f6f0b98f`.

> Nde4605c89d3cdd2fc4ed is a subregion of N04980f6d1f81f0aefb91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6ae5922c2a4aebab2026** — unrelated distractor; assertion `E14b87315d905248221c7`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `b7bdc0ad7cf5442add647013ec2184496f3ce99897c32fc61906a4232af8ee23`.

> Nde4605c89d3cdd2fc4ed is a subregion of N0d9c5caa04e6347c154b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4095.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C221076261f1c382e4bda

Pair: **F10001** / partner **C42bbd4765e6d5519d2b2**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N4142a55c2d046b158499? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E862736b3cc7957c1db38` from `D2c1207b84caee439eeea`: `N4142a55c2d046b158499 --NOT SUBREGION_OF--> N2bdb8e0081aea98b6bb5`.

Canonical positive-chain target: `Ne66dd9afcc8a121e916d`. Denied object: `N2bdb8e0081aea98b6bb5`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N4142a55c2d046b158499 --SUBREGION_OF [E3e90a150a45dd2fccc6d; D76413fefe6657c0277f5]--> Ne66dd9afcc8a121e916d
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D76413fefe6657c0277f5** — shortest-path support; assertion `E3e90a150a45dd2fccc6d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `bc271fd4000b30abddd0babfb6b73428b46eb189eefa9a807973c96041616d39`.

> N4142a55c2d046b158499 is a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2c1207b84caee439eeea** — explicit denial; assertion `E862736b3cc7957c1db38`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `59cf39e45762a6ed20e400f1db388e4d66f7d08ce03bacd4754c745244008fe2`.

> N4142a55c2d046b158499 is not a subregion of N2bdb8e0081aea98b6bb5. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db8ef2d8f24e3cb70b9e7** — unrelated distractor; assertion `E08abfde37c7fce6d7036`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1c86873eb89cf1af9be18ffea32823ffc1a178ab074a474329e23d05f6f0b98f`.

> Nde4605c89d3cdd2fc4ed is a subregion of N04980f6d1f81f0aefb91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6ae5922c2a4aebab2026** — unrelated distractor; assertion `E14b87315d905248221c7`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `b7bdc0ad7cf5442add647013ec2184496f3ce99897c32fc61906a4232af8ee23`.

> Nde4605c89d3cdd2fc4ed is a subregion of N0d9c5caa04e6347c154b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4081.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cdfdb9e95adde8d038e30

Pair: **F10002** / partner **C9ff35c7464e3e294054b**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nb7e9348d316c6a286896? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E36263343311e261efcca` from `De86dcf6f0a1c8071d14f`: `Nb7e9348d316c6a286896 --NOT PRECEDES--> N0c65c4abc3b732a7934d`.

Canonical positive-chain target: `N0c65c4abc3b732a7934d`. Denied object: `N0c65c4abc3b732a7934d`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nb7e9348d316c6a286896 --PRECEDES [E4ba418d64c723e906bac; Dc91305e56ad8347c54e2]--> N0c65c4abc3b732a7934d
```

Conflict witness sets (support plus separate denial): `[["E36263343311e261efcca","E4ba418d64c723e906bac"]]`.

### Source documents (verbatim)

**Dc91305e56ad8347c54e2** — shortest-path support; assertion `E4ba418d64c723e906bac`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `aebcc2d1fa2b69a0fabc0752fbc8703b7e0fad5d20d47c64153c3dfc44f6a180`.

> Nb7e9348d316c6a286896 precedes N0c65c4abc3b732a7934d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De86dcf6f0a1c8071d14f** — explicit denial; assertion `E36263343311e261efcca`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `38c96e37ada9112fe3244b49b3f000f210582417b5de71c74a500f49f14ab735`.

> Nb7e9348d316c6a286896 does not precede N0c65c4abc3b732a7934d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcecdd5235c39808adf00** — unrelated distractor; assertion `Ebd43d23d374ece50fa88`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `fe2954e5f1fe5898a8baf6c0e71c997b7e4c9a4a6a906fd3479524dccb896f77`.

> N76aeeb51a7c9ddb875d5 precedes N53efff33c7b277554005. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D096bf190fbd39b1198a9** — unrelated distractor; assertion `E2fc954e2cebbf0979e61`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `4366e73a64721238fd7352a02a6698fc7b69616bb6182e6daf8637ad9822526c`.

> N76aeeb51a7c9ddb875d5 precedes N84c4090907f73e3c23fe. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4090.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C9ff35c7464e3e294054b

Pair: **F10002** / partner **Cdfdb9e95adde8d038e30**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nb7e9348d316c6a286896? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ef7d3448108348e755a98` from `D05bcb6c31f6fea61f984`: `Nb7e9348d316c6a286896 --NOT PRECEDES--> N33d30953b22ca6263bc3`.

Canonical positive-chain target: `N0c65c4abc3b732a7934d`. Denied object: `N33d30953b22ca6263bc3`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nb7e9348d316c6a286896 --PRECEDES [E4ba418d64c723e906bac; Dc91305e56ad8347c54e2]--> N0c65c4abc3b732a7934d
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Dc91305e56ad8347c54e2** — shortest-path support; assertion `E4ba418d64c723e906bac`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `aebcc2d1fa2b69a0fabc0752fbc8703b7e0fad5d20d47c64153c3dfc44f6a180`.

> Nb7e9348d316c6a286896 precedes N0c65c4abc3b732a7934d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D05bcb6c31f6fea61f984** — explicit denial; assertion `Ef7d3448108348e755a98`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `1d9609ac9b0c683154aeda306513122c650dfb5609292b66ad48b95d2e2ba70d`.

> Nb7e9348d316c6a286896 does not precede N33d30953b22ca6263bc3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcecdd5235c39808adf00** — unrelated distractor; assertion `Ebd43d23d374ece50fa88`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `fe2954e5f1fe5898a8baf6c0e71c997b7e4c9a4a6a906fd3479524dccb896f77`.

> N76aeeb51a7c9ddb875d5 precedes N53efff33c7b277554005. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D096bf190fbd39b1198a9** — unrelated distractor; assertion `E2fc954e2cebbf0979e61`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `4366e73a64721238fd7352a02a6698fc7b69616bb6182e6daf8637ad9822526c`.

> N76aeeb51a7c9ddb875d5 precedes N84c4090907f73e3c23fe. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4087.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cec8bb9e3d570ee94ba8e

Pair: **F10003** / partner **Cbe622777f555a0d79985**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N5c25ba15012717d75075? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ee69bcd181d8f02cb0da9` from `Df5eb887b15569304836e`: `N5c25ba15012717d75075 --NOT CONTAINED_IN--> N8b16c886321739295ac2`.

Canonical positive-chain target: `N8b16c886321739295ac2`. Denied object: `N8b16c886321739295ac2`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N5c25ba15012717d75075 --CONTAINED_IN [E448e147fed83e7429c99; D9af1d40ddbb5b93c6ddf]--> N8b16c886321739295ac2
```

Conflict witness sets (support plus separate denial): `[["E448e147fed83e7429c99","Ee69bcd181d8f02cb0da9"]]`.

### Source documents (verbatim)

**D9af1d40ddbb5b93c6ddf** — shortest-path support; assertion `E448e147fed83e7429c99`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `06722013d13630683bafda8419d5c7da10880c0f27f6bd94961e413c7ec47590`.

> N5c25ba15012717d75075 is contained in N8b16c886321739295ac2. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df5eb887b15569304836e** — explicit denial; assertion `Ee69bcd181d8f02cb0da9`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `c70b82f37b8f6d1c34daad91d3fb30fd659fe65ca1489bd4649779da79a699a0`.

> N5c25ba15012717d75075 is not contained in N8b16c886321739295ac2. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D87e6c533b79da8158b89** — unrelated distractor; assertion `E55df4e889dc84883f7d3`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `7ca0c60ba0633822c1f09e75a5ed6c51f90a623115773f6596ebccfc057f4009`.

> N6f3308560cee97d3b9e5 is contained in Na45fe2dc5514ade260d4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De4e2983cbee815e6065b** — unrelated distractor; assertion `E1bf84a5d5a0ef5f35f90`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `8a813c8c11168b23a5b357e61764e2fc2ec12d3e1977ce3a5694de8faa158c41`.

> N6f3308560cee97d3b9e5 is contained in N25bda654e37ec2f0a046. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4096.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cbe622777f555a0d79985

Pair: **F10003** / partner **Cec8bb9e3d570ee94ba8e**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N5c25ba15012717d75075? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E799c17f321285a4a272e` from `Decdf71c98e5febd35406`: `N5c25ba15012717d75075 --NOT CONTAINED_IN--> Nd2294682e2ec4953756e`.

Canonical positive-chain target: `N8b16c886321739295ac2`. Denied object: `Nd2294682e2ec4953756e`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N5c25ba15012717d75075 --CONTAINED_IN [E448e147fed83e7429c99; D9af1d40ddbb5b93c6ddf]--> N8b16c886321739295ac2
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D9af1d40ddbb5b93c6ddf** — shortest-path support; assertion `E448e147fed83e7429c99`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `06722013d13630683bafda8419d5c7da10880c0f27f6bd94961e413c7ec47590`.

> N5c25ba15012717d75075 is contained in N8b16c886321739295ac2. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Decdf71c98e5febd35406** — explicit denial; assertion `E799c17f321285a4a272e`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `61971a28fe2f2cc03b7aae809b03bad1bd874702989f48faef8f251e412548eb`.

> N5c25ba15012717d75075 is not contained in Nd2294682e2ec4953756e. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D87e6c533b79da8158b89** — unrelated distractor; assertion `E55df4e889dc84883f7d3`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `7ca0c60ba0633822c1f09e75a5ed6c51f90a623115773f6596ebccfc057f4009`.

> N6f3308560cee97d3b9e5 is contained in Na45fe2dc5514ade260d4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De4e2983cbee815e6065b** — unrelated distractor; assertion `E1bf84a5d5a0ef5f35f90`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `8a813c8c11168b23a5b357e61764e2fc2ec12d3e1977ce3a5694de8faa158c41`.

> N6f3308560cee97d3b9e5 is contained in N25bda654e37ec2f0a046. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4090.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C45be00a9a7ad99b996ad

Pair: **F10004** / partner **Cb5f1498885e5977e31a0**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N324f143dbc083c31fae5? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Eeba15ded9e9c51bc0b8c` from `D0a16265bee860bd48511`: `N324f143dbc083c31fae5 --NOT SUBREGION_OF--> N813f098a1c1b15ccbe6e`.

Canonical positive-chain target: `N813f098a1c1b15ccbe6e`. Denied object: `N813f098a1c1b15ccbe6e`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N324f143dbc083c31fae5 --SUBREGION_OF [Ec1ec15923e457c98b27d; D375355d9484fbf6d0145]--> N813f098a1c1b15ccbe6e
```

Conflict witness sets (support plus separate denial): `[["Ec1ec15923e457c98b27d","Eeba15ded9e9c51bc0b8c"]]`.

### Source documents (verbatim)

**D375355d9484fbf6d0145** — shortest-path support; assertion `Ec1ec15923e457c98b27d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `747c3e5ce18abf312c3233ee2c270c0d4783a5355fd7cade88a87902690ab7ac`.

> N324f143dbc083c31fae5 is a subregion of N813f098a1c1b15ccbe6e. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D0a16265bee860bd48511** — explicit denial; assertion `Eeba15ded9e9c51bc0b8c`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `68c51d33d084baeef93585fc5210f58e226685bce765ac70e6e81ce997232806`.

> N324f143dbc083c31fae5 is not a subregion of N813f098a1c1b15ccbe6e. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D813a5727276cc4bd97d1** — unrelated distractor; assertion `E1f17bdd0285048fcc440`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `0cc121c6a05c46c36cc716409b4ad6cfc51cf8d821beb06be2cdea74d5558ff6`.

> N394641f8aa4c154a2289 is a subregion of N5feecaf16ad1883937a8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dc3ec77827ceea4dcff0a** — unrelated distractor; assertion `Ed8abc24c5e02a0b05ccc`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2d9ce4318c4b4bc0ab47c6620781e4d6f5806e7156a1a0a2ee414baf74b88d0b`.

> N394641f8aa4c154a2289 is a subregion of Ne3baeb4e132f3fbdb536. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4080.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cb5f1498885e5977e31a0

Pair: **F10004** / partner **C45be00a9a7ad99b996ad**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N324f143dbc083c31fae5? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E764285df7deca203954c` from `Dc8e09dd6425c669a282f`: `N324f143dbc083c31fae5 --NOT SUBREGION_OF--> Nba0947532222bd792458`.

Canonical positive-chain target: `N813f098a1c1b15ccbe6e`. Denied object: `Nba0947532222bd792458`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N324f143dbc083c31fae5 --SUBREGION_OF [Ec1ec15923e457c98b27d; D375355d9484fbf6d0145]--> N813f098a1c1b15ccbe6e
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D375355d9484fbf6d0145** — shortest-path support; assertion `Ec1ec15923e457c98b27d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `747c3e5ce18abf312c3233ee2c270c0d4783a5355fd7cade88a87902690ab7ac`.

> N324f143dbc083c31fae5 is a subregion of N813f098a1c1b15ccbe6e. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dc8e09dd6425c669a282f** — explicit denial; assertion `E764285df7deca203954c`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `8f9d46cf9124560a0e238ac14986e0af0bdc5bb9957de5067db5649cfb29d929`.

> N324f143dbc083c31fae5 is not a subregion of Nba0947532222bd792458. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D813a5727276cc4bd97d1** — unrelated distractor; assertion `E1f17bdd0285048fcc440`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `0cc121c6a05c46c36cc716409b4ad6cfc51cf8d821beb06be2cdea74d5558ff6`.

> N394641f8aa4c154a2289 is a subregion of N5feecaf16ad1883937a8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dc3ec77827ceea4dcff0a** — unrelated distractor; assertion `Ed8abc24c5e02a0b05ccc`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2d9ce4318c4b4bc0ab47c6620781e4d6f5806e7156a1a0a2ee414baf74b88d0b`.

> N394641f8aa4c154a2289 is a subregion of Ne3baeb4e132f3fbdb536. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 35; delivered: 35; evidence tokens: 4093.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Ceb082b2014ab0733ca7c

Pair: **F10005** / partner **C9d23b5521dfd594f827d**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd66233e3482844959e22? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ecdb3e3f50cd0ac3a98f1` from `Ddd90b4110e833cad50f5`: `Nd66233e3482844959e22 --NOT PRECEDES--> N9172d66180b0534b3189`.

Canonical positive-chain target: `N9172d66180b0534b3189`. Denied object: `N9172d66180b0534b3189`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nd66233e3482844959e22 --PRECEDES [E9369880e788ed59aac90; D307f61e2bb61c65dbffa]--> N9172d66180b0534b3189
```

Conflict witness sets (support plus separate denial): `[["E9369880e788ed59aac90","Ecdb3e3f50cd0ac3a98f1"]]`.

### Source documents (verbatim)

**D307f61e2bb61c65dbffa** — shortest-path support; assertion `E9369880e788ed59aac90`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `dd119d99ded6feb48b873a85e07aaa5e846f28208190a1fedfa4d3a31121a9f2`.

> Nd66233e3482844959e22 precedes N9172d66180b0534b3189. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Ddd90b4110e833cad50f5** — explicit denial; assertion `Ecdb3e3f50cd0ac3a98f1`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `03d4aa40e96bac8688a9342e42143c067c3ded51f801f03b46f10ce8a752122d`.

> Nd66233e3482844959e22 does not precede N9172d66180b0534b3189. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df08f83e6fbc691cf3e31** — unrelated distractor; assertion `Ed4ff04400c5f71b45bf9`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `b540a7ec122bbab0869c6694fa3bdc293020a474bb745fe18bc40a84cab4fac4`.

> Nf8b1c7505d9b986a8b38 precedes N0a1e47343b8c7af38d5a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D871bca2b3ebe8857e3c7** — unrelated distractor; assertion `E91e6c640aebda801efb8`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `a0580358fe9ce39001c1e348bdc5fc116f020b9b686d0ca35e03488ff308edf2`.

> Nf8b1c7505d9b986a8b38 precedes N3a17ed1d7b8c474915fd. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4087.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C9d23b5521dfd594f827d

Pair: **F10005** / partner **Ceb082b2014ab0733ca7c**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd66233e3482844959e22? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E07d7cb5c367937a74fcd` from `D9ef8a07e4e94f4e5961c`: `Nd66233e3482844959e22 --NOT PRECEDES--> Nd2957dc95a4e5305bcec`.

Canonical positive-chain target: `N9172d66180b0534b3189`. Denied object: `Nd2957dc95a4e5305bcec`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nd66233e3482844959e22 --PRECEDES [E9369880e788ed59aac90; D307f61e2bb61c65dbffa]--> N9172d66180b0534b3189
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D307f61e2bb61c65dbffa** — shortest-path support; assertion `E9369880e788ed59aac90`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `dd119d99ded6feb48b873a85e07aaa5e846f28208190a1fedfa4d3a31121a9f2`.

> Nd66233e3482844959e22 precedes N9172d66180b0534b3189. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D9ef8a07e4e94f4e5961c** — explicit denial; assertion `E07d7cb5c367937a74fcd`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `fb543007d971c4e3004a359345f47afb1690788ecde3114fd0fea47b4489f76b`.

> Nd66233e3482844959e22 does not precede Nd2957dc95a4e5305bcec. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df08f83e6fbc691cf3e31** — unrelated distractor; assertion `Ed4ff04400c5f71b45bf9`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `b540a7ec122bbab0869c6694fa3bdc293020a474bb745fe18bc40a84cab4fac4`.

> Nf8b1c7505d9b986a8b38 precedes N0a1e47343b8c7af38d5a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D871bca2b3ebe8857e3c7** — unrelated distractor; assertion `E91e6c640aebda801efb8`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `a0580358fe9ce39001c1e348bdc5fc116f020b9b686d0ca35e03488ff308edf2`.

> Nf8b1c7505d9b986a8b38 precedes N3a17ed1d7b8c474915fd. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4080.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cdfa0fc2ed7b9fb7e49cb

Pair: **F10006** / partner **C05c58bea507790542472**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N923e335cbc8216e66c64? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ec139c2f22630f15a79ae` from `D10aa6c96159963cc11c5`: `N923e335cbc8216e66c64 --NOT CONTAINED_IN--> N1e8fcad3204036505b14`.

Canonical positive-chain target: `N1e8fcad3204036505b14`. Denied object: `N1e8fcad3204036505b14`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N923e335cbc8216e66c64 --CONTAINED_IN [Eba23f791661942aa4d59; Dbae378b505543854ddd0]--> N1e8fcad3204036505b14
```

Conflict witness sets (support plus separate denial): `[["Eba23f791661942aa4d59","Ec139c2f22630f15a79ae"]]`.

### Source documents (verbatim)

**Dbae378b505543854ddd0** — shortest-path support; assertion `Eba23f791661942aa4d59`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `ac275d9a4afa1b7a4328422a8402047d28897a8724c88c3cf568a9f04868a844`.

> N923e335cbc8216e66c64 is contained in N1e8fcad3204036505b14. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D10aa6c96159963cc11c5** — explicit denial; assertion `Ec139c2f22630f15a79ae`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `9f9ce113e36c4e4981f2506df96ae72d4dcac1193758b1224fa4ea3e48225a4d`.

> N923e335cbc8216e66c64 is not contained in N1e8fcad3204036505b14. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd9fb9c37159b590d129d** — unrelated distractor; assertion `E7a0faf4a19969436b7ea`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `e7eb46275cbfe4bc914dd0d3584d5bf29cfdc7c658bb765fb7daa95d645ffeb6`.

> N8b368e8ce401a33308d5 is contained in Na2022016b5a2dce20bf4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfa8525393f12be468392** — unrelated distractor; assertion `Ef12d3f129d7481c48a91`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `86b5656bd7465fe6e6dce11856958f420dcb1089bb6f4666bd428ed8c56ec7f1`.

> N8b368e8ce401a33308d5 is contained in Ne141e08ab8016fa7e93a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4093.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C05c58bea507790542472

Pair: **F10006** / partner **Cdfa0fc2ed7b9fb7e49cb**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N923e335cbc8216e66c64? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E8915e62a244f444e98fc` from `D1480b1ec511eb927e1f0`: `N923e335cbc8216e66c64 --NOT CONTAINED_IN--> N96432f28eee459ff376b`.

Canonical positive-chain target: `N1e8fcad3204036505b14`. Denied object: `N96432f28eee459ff376b`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
N923e335cbc8216e66c64 --CONTAINED_IN [Eba23f791661942aa4d59; Dbae378b505543854ddd0]--> N1e8fcad3204036505b14
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Dbae378b505543854ddd0** — shortest-path support; assertion `Eba23f791661942aa4d59`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `ac275d9a4afa1b7a4328422a8402047d28897a8724c88c3cf568a9f04868a844`.

> N923e335cbc8216e66c64 is contained in N1e8fcad3204036505b14. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D1480b1ec511eb927e1f0** — explicit denial; assertion `E8915e62a244f444e98fc`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `42fe566c9279249963664fd6a09f536761c2c5ec93a29d81e837dd22b2ea3855`.

> N923e335cbc8216e66c64 is not contained in N96432f28eee459ff376b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd9fb9c37159b590d129d** — unrelated distractor; assertion `E7a0faf4a19969436b7ea`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `e7eb46275cbfe4bc914dd0d3584d5bf29cfdc7c658bb765fb7daa95d645ffeb6`.

> N8b368e8ce401a33308d5 is contained in Na2022016b5a2dce20bf4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfa8525393f12be468392** — unrelated distractor; assertion `Ef12d3f129d7481c48a91`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `86b5656bd7465fe6e6dce11856958f420dcb1089bb6f4666bd428ed8c56ec7f1`.

> N8b368e8ce401a33308d5 is contained in Ne141e08ab8016fa7e93a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4085.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cdb61bd674a8718cdab06

Pair: **F10007** / partner **Ce9e17b943ef1908e97e1**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nfdd9917e2c8514e36790? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ed61c0ec415d5a0db6a44` from `De23b7cd8d19e6364adcf`: `Nfdd9917e2c8514e36790 --NOT SUBREGION_OF--> N54cdc918ea4a9e4429d6`.

Canonical positive-chain target: `N54cdc918ea4a9e4429d6`. Denied object: `N54cdc918ea4a9e4429d6`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nfdd9917e2c8514e36790 --SUBREGION_OF [E9a394e24cff498cdbf6d; D012c0031b1c2d5f5b85e]--> N54cdc918ea4a9e4429d6
```

Conflict witness sets (support plus separate denial): `[["E9a394e24cff498cdbf6d","Ed61c0ec415d5a0db6a44"]]`.

### Source documents (verbatim)

**D012c0031b1c2d5f5b85e** — shortest-path support; assertion `E9a394e24cff498cdbf6d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `118fafcff2e74462998c2ef92eaddda3b4534ce1d66a415cb4349267d9a70f52`.

> Nfdd9917e2c8514e36790 is a subregion of N54cdc918ea4a9e4429d6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De23b7cd8d19e6364adcf** — explicit denial; assertion `Ed61c0ec415d5a0db6a44`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `7b8a9f8b3ea27634f7e68c7a526316ac414f2f34eee02fddf16f14eee0c37566`.

> Nfdd9917e2c8514e36790 is not a subregion of N54cdc918ea4a9e4429d6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D0315265825c4b1410658** — unrelated distractor; assertion `Eeb95513cddc65779bf0f`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a7acaa4a5e52a45d19b883276cb614e2362004fc65eb53ab754c2c70090aad84`.

> N7ce66bd22c354bc1a9e5 is a subregion of Nec00b3ac713c6ce591a0. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db2bea032f721a1121d41** — unrelated distractor; assertion `Ef6433d48e4db9071bab4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2fb9943644c21bdb215f9df3a5909b21d2e7a0e984cea7b1f8b97d642836a7dd`.

> N7ce66bd22c354bc1a9e5 is a subregion of Nfe39df2af3064056734d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4092.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; positive_and_denial_share_one_undirected_native_edge.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Ce9e17b943ef1908e97e1

Pair: **F10007** / partner **Cdb61bd674a8718cdab06**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **1**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nfdd9917e2c8514e36790? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ed1ac85f2730336f9c608` from `D3148c187fee308bd07c7`: `Nfdd9917e2c8514e36790 --NOT SUBREGION_OF--> Na5bfbdc8502eb2b0f923`.

Canonical positive-chain target: `N54cdc918ea4a9e4429d6`. Denied object: `Na5bfbdc8502eb2b0f923`.

### All shortest positive source-backed paths

Path 1 (1 supporting hops):

```text
Nfdd9917e2c8514e36790 --SUBREGION_OF [E9a394e24cff498cdbf6d; D012c0031b1c2d5f5b85e]--> N54cdc918ea4a9e4429d6
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D012c0031b1c2d5f5b85e** — shortest-path support; assertion `E9a394e24cff498cdbf6d`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `118fafcff2e74462998c2ef92eaddda3b4534ce1d66a415cb4349267d9a70f52`.

> Nfdd9917e2c8514e36790 is a subregion of N54cdc918ea4a9e4429d6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3148c187fee308bd07c7** — explicit denial; assertion `Ed1ac85f2730336f9c608`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `722ecfa0f5cc0960497e54660d01862f9cf8e9da44e2d326d4476ee733cd4708`.

> Nfdd9917e2c8514e36790 is not a subregion of Na5bfbdc8502eb2b0f923. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D0315265825c4b1410658** — unrelated distractor; assertion `Eeb95513cddc65779bf0f`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a7acaa4a5e52a45d19b883276cb614e2362004fc65eb53ab754c2c70090aad84`.

> N7ce66bd22c354bc1a9e5 is a subregion of Nec00b3ac713c6ce591a0. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db2bea032f721a1121d41** — unrelated distractor; assertion `Ef6433d48e4db9071bab4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2fb9943644c21bdb215f9df3a5909b21d2e7a0e984cea7b1f8b97d642836a7dd`.

> N7ce66bd22c354bc1a9e5 is a subregion of Nfe39df2af3064056734d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4083.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C7e7d62477508e2b4388a

Pair: **F20000** / partner **C4bd4688564a242ecf137**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N9e542f5f0372f5925428? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E60bdd836c6fd415b8ae7` from `D484ceaf31f69109851b6`: `N9e542f5f0372f5925428 --NOT CONTAINED_IN--> Nce7afaa048239899b51b`.

Canonical positive-chain target: `Nce7afaa048239899b51b`. Denied object: `Nce7afaa048239899b51b`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N9e542f5f0372f5925428 --CONTAINED_IN [E5228caa11684d9ab73cb; Dacb8c3df2f00f4b6989f]--> Neba37e9f6d5110819858 --CONTAINED_IN [Ee478f8ff67b9f5b66b4e; Df64f894e1735c6e17ae6]--> Nce7afaa048239899b51b
```

Conflict witness sets (support plus separate denial): `[["E5228caa11684d9ab73cb","E60bdd836c6fd415b8ae7","Ee478f8ff67b9f5b66b4e"]]`.

### Source documents (verbatim)

**Dacb8c3df2f00f4b6989f** — shortest-path support; assertion `E5228caa11684d9ab73cb`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `584340e41e4bd2645d5f6acb991ee0c0eccb9887edfe6be8bba75b33f50d2bfc`.

> N9e542f5f0372f5925428 is contained in Neba37e9f6d5110819858. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df64f894e1735c6e17ae6** — shortest-path support; assertion `Ee478f8ff67b9f5b66b4e`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c3b6cf35baec0dfe9dd202dfbed107121776ee098ca80a29db054a78182223ba`.

> Neba37e9f6d5110819858 is contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D484ceaf31f69109851b6** — explicit denial; assertion `E60bdd836c6fd415b8ae7`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `382cfc997cd5489f425ec61abc4f6afe7c2f86b6c2b81c72dd785b15312be613`.

> N9e542f5f0372f5925428 is not contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D36fb5058c4a46729efa4** — unrelated distractor; assertion `E52315cd3dae63cfc3416`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `05c5e34d0a5524008609769f8c9e2ececa1f7c01e5eb6615d5c25b41fe73dd87`.

> N0b786528fec79853affc is contained in N48d8423b237f1065adf8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2934e038681cf53c6fbd** — unrelated distractor; assertion `E3e1a359b24d05c3477cc`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `7c4d62c1343ff29359194a643ed31dad0e8d5538943ff4e28e3ad0c5f0302d00`.

> N0b786528fec79853affc is contained in N6d9ef794a20ca01bae91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 38; delivered: 38; evidence tokens: 4093.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C4bd4688564a242ecf137

Pair: **F20000** / partner **C7e7d62477508e2b4388a**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N9e542f5f0372f5925428? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E3943e4e4c2e3ed13b5ed` from `D39a8e0b264a8fdfff918`: `N9e542f5f0372f5925428 --NOT CONTAINED_IN--> N746149004f1f40df0cdc`.

Canonical positive-chain target: `Nce7afaa048239899b51b`. Denied object: `N746149004f1f40df0cdc`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N9e542f5f0372f5925428 --CONTAINED_IN [E5228caa11684d9ab73cb; Dacb8c3df2f00f4b6989f]--> Neba37e9f6d5110819858 --CONTAINED_IN [Ee478f8ff67b9f5b66b4e; Df64f894e1735c6e17ae6]--> Nce7afaa048239899b51b
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Dacb8c3df2f00f4b6989f** — shortest-path support; assertion `E5228caa11684d9ab73cb`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `584340e41e4bd2645d5f6acb991ee0c0eccb9887edfe6be8bba75b33f50d2bfc`.

> N9e542f5f0372f5925428 is contained in Neba37e9f6d5110819858. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df64f894e1735c6e17ae6** — shortest-path support; assertion `Ee478f8ff67b9f5b66b4e`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c3b6cf35baec0dfe9dd202dfbed107121776ee098ca80a29db054a78182223ba`.

> Neba37e9f6d5110819858 is contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D39a8e0b264a8fdfff918** — explicit denial; assertion `E3943e4e4c2e3ed13b5ed`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `b4263d9c70d8be00ee340d458075e1e5a7cc99548b6abf73a1d82609632ad4ce`.

> N9e542f5f0372f5925428 is not contained in N746149004f1f40df0cdc. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D36fb5058c4a46729efa4** — unrelated distractor; assertion `E52315cd3dae63cfc3416`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `05c5e34d0a5524008609769f8c9e2ececa1f7c01e5eb6615d5c25b41fe73dd87`.

> N0b786528fec79853affc is contained in N48d8423b237f1065adf8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2934e038681cf53c6fbd** — unrelated distractor; assertion `E3e1a359b24d05c3477cc`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `7c4d62c1343ff29359194a643ed31dad0e8d5538943ff4e28e3ad0c5f0302d00`.

> N0b786528fec79853affc is contained in N6d9ef794a20ca01bae91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C7ea8d2cba383bd89ac9d

Pair: **F20001** / partner **C5ef6d9ade86682fff037**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nc2c0024edfa5578510dc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E12865dea098d8cc7644e` from `Da175516fb4d2dd15b1c8`: `Nc2c0024edfa5578510dc --NOT SUBREGION_OF--> N73aab90ad43a1c44d8b8`.

Canonical positive-chain target: `N73aab90ad43a1c44d8b8`. Denied object: `N73aab90ad43a1c44d8b8`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
Nc2c0024edfa5578510dc --SUBREGION_OF [Efe8826c33f9cedcec848; D79e87d2f4d1f958bca1f]--> Nb311850e0d6f1dfede25 --SUBREGION_OF [Eb8b66fb63a602b3a9e54; De251762bf8dc191c5046]--> N73aab90ad43a1c44d8b8
```

Conflict witness sets (support plus separate denial): `[["E12865dea098d8cc7644e","Eb8b66fb63a602b3a9e54","Efe8826c33f9cedcec848"]]`.

### Source documents (verbatim)

**D79e87d2f4d1f958bca1f** — shortest-path support; assertion `Efe8826c33f9cedcec848`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `6015dc73f2dffde830ae47264e54b4c08f2203eeaf821876be7630d6e9620964`.

> Nc2c0024edfa5578510dc is a subregion of Nb311850e0d6f1dfede25. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De251762bf8dc191c5046** — shortest-path support; assertion `Eb8b66fb63a602b3a9e54`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `176035cddbce8def06e6d53f96cbd343f4d7ba9b6703f20563ff51dafacd52a9`.

> Nb311850e0d6f1dfede25 is a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da175516fb4d2dd15b1c8** — explicit denial; assertion `E12865dea098d8cc7644e`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `c9a1a54ee8408c1ebaa19a0ace414f630b9f7f3cd00e289b1c39f3df8ef53c2d`.

> Nc2c0024edfa5578510dc is not a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D53dcc127c5efac8b5871** — unrelated distractor; assertion `Ef53084aea6273d93ed51`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a4cccd2940365bb9f113dc085b05ceae0d4dbc00c16b96749e848e6ff4c0fa56`.

> N5527bdf69bd05b287e26 is a subregion of Nb2c5d62a052f8aef12e6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da7d93ca64ddb2385286a** — unrelated distractor; assertion `E41b203a9154b3d35796f`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `fa91217c1c3a7ffbf6764ea7e88bae3186b2140c8463d1f7cd6e66087749a6a5`.

> N5527bdf69bd05b287e26 is a subregion of N35e91e1cecb1ca1d2d0c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 40; delivered: 40; evidence tokens: 4079.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C5ef6d9ade86682fff037

Pair: **F20001** / partner **C7ea8d2cba383bd89ac9d**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nc2c0024edfa5578510dc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E48989830b3204a80c126` from `D3ef4f03e9b791e37b6ba`: `Nc2c0024edfa5578510dc --NOT SUBREGION_OF--> Nc47ab82c165a565a2337`.

Canonical positive-chain target: `N73aab90ad43a1c44d8b8`. Denied object: `Nc47ab82c165a565a2337`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
Nc2c0024edfa5578510dc --SUBREGION_OF [Efe8826c33f9cedcec848; D79e87d2f4d1f958bca1f]--> Nb311850e0d6f1dfede25 --SUBREGION_OF [Eb8b66fb63a602b3a9e54; De251762bf8dc191c5046]--> N73aab90ad43a1c44d8b8
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D79e87d2f4d1f958bca1f** — shortest-path support; assertion `Efe8826c33f9cedcec848`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `6015dc73f2dffde830ae47264e54b4c08f2203eeaf821876be7630d6e9620964`.

> Nc2c0024edfa5578510dc is a subregion of Nb311850e0d6f1dfede25. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De251762bf8dc191c5046** — shortest-path support; assertion `Eb8b66fb63a602b3a9e54`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `176035cddbce8def06e6d53f96cbd343f4d7ba9b6703f20563ff51dafacd52a9`.

> Nb311850e0d6f1dfede25 is a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3ef4f03e9b791e37b6ba** — explicit denial; assertion `E48989830b3204a80c126`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `66c4dadd0744b47bd769a3a39c44699316927e37d71ac9d4e08f75be91726bb7`.

> Nc2c0024edfa5578510dc is not a subregion of Nc47ab82c165a565a2337. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D53dcc127c5efac8b5871** — unrelated distractor; assertion `Ef53084aea6273d93ed51`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a4cccd2940365bb9f113dc085b05ceae0d4dbc00c16b96749e848e6ff4c0fa56`.

> N5527bdf69bd05b287e26 is a subregion of Nb2c5d62a052f8aef12e6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da7d93ca64ddb2385286a** — unrelated distractor; assertion `E41b203a9154b3d35796f`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `fa91217c1c3a7ffbf6764ea7e88bae3186b2140c8463d1f7cd6e66087749a6a5`.

> N5527bdf69bd05b287e26 is a subregion of N35e91e1cecb1ca1d2d0c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C284858966dec17b70c96

Pair: **F20002** / partner **C85bfbe12307f7f880a90**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N77f50f6eccafe2ccf18c? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ef8d529946d7970ee72f2` from `D3987590ecfb6040326d8`: `N77f50f6eccafe2ccf18c --NOT PRECEDES--> Nbc1e5d973b720d379e08`.

Canonical positive-chain target: `Nbc1e5d973b720d379e08`. Denied object: `Nbc1e5d973b720d379e08`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N77f50f6eccafe2ccf18c --PRECEDES [E8f40d441db6c2c7f1438; Db9e4de6b351db6a50856]--> Nd346fd5ffa2c8ee1067b --PRECEDES [E44b01fdf9b58f0708408; Deb75e238ae54da5ebf3e]--> Nbc1e5d973b720d379e08
```

Conflict witness sets (support plus separate denial): `[["E44b01fdf9b58f0708408","E8f40d441db6c2c7f1438","Ef8d529946d7970ee72f2"]]`.

### Source documents (verbatim)

**Db9e4de6b351db6a50856** — shortest-path support; assertion `E8f40d441db6c2c7f1438`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `3b9ee07f6dc741415251fe829b891d77912e9c9234036186599c7323f971e3ee`.

> N77f50f6eccafe2ccf18c precedes Nd346fd5ffa2c8ee1067b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Deb75e238ae54da5ebf3e** — shortest-path support; assertion `E44b01fdf9b58f0708408`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `506325bc00ed29acdca9919ab6d7378fb72d3d824c9b9614e5f6fde1727b0df5`.

> Nd346fd5ffa2c8ee1067b precedes Nbc1e5d973b720d379e08. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3987590ecfb6040326d8** — explicit denial; assertion `Ef8d529946d7970ee72f2`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `857381d676ad67c2b7017e8349f3069f04a7dc2db7f55bb0f40ad9a6ffb530a1`.

> N77f50f6eccafe2ccf18c does not precede Nbc1e5d973b720d379e08. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De3f35bb5cd2daf23678e** — unrelated distractor; assertion `E469803419936cc5b4633`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `448b41271d07f14be230ff0c68800f82d76a104a961131751c87f0750af3fce5`.

> Ncbb3d58bd325d505e920 precedes N961ec60d0a387f13599d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De791e97b2b1adf07df4f** — unrelated distractor; assertion `Eb83ae5e673752823c88d`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `0bb2083bfd955925c12303367b118c8eb18bfbe08661e6b8b39f6893dda398c2`.

> Ncbb3d58bd325d505e920 precedes Nefd4733e55e655e415d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 37; delivered: 37; evidence tokens: 4095.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C85bfbe12307f7f880a90

Pair: **F20002** / partner **C284858966dec17b70c96**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N77f50f6eccafe2ccf18c? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E5077f89b9e44f5c5748b` from `Dc9320332e07435936dd6`: `N77f50f6eccafe2ccf18c --NOT PRECEDES--> Nf64635cf939347738bb7`.

Canonical positive-chain target: `Nbc1e5d973b720d379e08`. Denied object: `Nf64635cf939347738bb7`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N77f50f6eccafe2ccf18c --PRECEDES [E8f40d441db6c2c7f1438; Db9e4de6b351db6a50856]--> Nd346fd5ffa2c8ee1067b --PRECEDES [E44b01fdf9b58f0708408; Deb75e238ae54da5ebf3e]--> Nbc1e5d973b720d379e08
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Db9e4de6b351db6a50856** — shortest-path support; assertion `E8f40d441db6c2c7f1438`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `3b9ee07f6dc741415251fe829b891d77912e9c9234036186599c7323f971e3ee`.

> N77f50f6eccafe2ccf18c precedes Nd346fd5ffa2c8ee1067b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Deb75e238ae54da5ebf3e** — shortest-path support; assertion `E44b01fdf9b58f0708408`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `506325bc00ed29acdca9919ab6d7378fb72d3d824c9b9614e5f6fde1727b0df5`.

> Nd346fd5ffa2c8ee1067b precedes Nbc1e5d973b720d379e08. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dc9320332e07435936dd6** — explicit denial; assertion `E5077f89b9e44f5c5748b`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `c13e84892573bba3604ed41d26ca8acec1cd4a5da67b270f43294f7564134412`.

> N77f50f6eccafe2ccf18c does not precede Nf64635cf939347738bb7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De3f35bb5cd2daf23678e** — unrelated distractor; assertion `E469803419936cc5b4633`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `448b41271d07f14be230ff0c68800f82d76a104a961131751c87f0750af3fce5`.

> Ncbb3d58bd325d505e920 precedes N961ec60d0a387f13599d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De791e97b2b1adf07df4f** — unrelated distractor; assertion `Eb83ae5e673752823c88d`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `0bb2083bfd955925c12303367b118c8eb18bfbe08661e6b8b39f6893dda398c2`.

> Ncbb3d58bd325d505e920 precedes Nefd4733e55e655e415d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4090.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C8df4eb422ddda77c47ec

Pair: **F20003** / partner **C6522cdd91136ea81cb55**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N68253ce6d9b195c5dacc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E38dfdd37f439a9fa0469` from `D1e6fcd119ed03eaa5770`: `N68253ce6d9b195c5dacc --NOT CONTAINED_IN--> Ncc69027d69c243c0f5a9`.

Canonical positive-chain target: `Ncc69027d69c243c0f5a9`. Denied object: `Ncc69027d69c243c0f5a9`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N68253ce6d9b195c5dacc --CONTAINED_IN [E510c678e2030565fc05c; Db4656d39a9d08594c964]--> N27a21b96b1491171f92c --CONTAINED_IN [E668516fa57e50e3cd88b; Dbb866ffea43863d04da8]--> Ncc69027d69c243c0f5a9
```

Conflict witness sets (support plus separate denial): `[["E38dfdd37f439a9fa0469","E510c678e2030565fc05c","E668516fa57e50e3cd88b"]]`.

### Source documents (verbatim)

**Db4656d39a9d08594c964** — shortest-path support; assertion `E510c678e2030565fc05c`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `f9295c1af59f8baeefdc2d24069fb36779a6b5e55d586309cae815629df3a206`.

> N68253ce6d9b195c5dacc is contained in N27a21b96b1491171f92c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dbb866ffea43863d04da8** — shortest-path support; assertion `E668516fa57e50e3cd88b`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c0ca39561f8261ab9263bc0d8c9012c1038e3309fd8edf4476fa7eefbc02dbf3`.

> N27a21b96b1491171f92c is contained in Ncc69027d69c243c0f5a9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D1e6fcd119ed03eaa5770** — explicit denial; assertion `E38dfdd37f439a9fa0469`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `f4e262907b77569a5d7c439c63d281da2c0d55a1e410f91ab67d5356f904a9c8`.

> N68253ce6d9b195c5dacc is not contained in Ncc69027d69c243c0f5a9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1960a17d8787a3b1cee** — unrelated distractor; assertion `E4d86338ce7247a29f4f4`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `e43f2536d7c19740fc04cddf41f66bc9a7a39196c313626825017daacf269f0f`.

> N93f78a4e6d0265362062 is contained in N099894cda8f2f6a2b5b2. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5e36db57ddaf9a79ea52** — unrelated distractor; assertion `Ecce47c2f80d249bbfde1`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `1e7742ae21de7409ad308b4090b9ecf478797233e174f546da54f4dee2baa35a`.

> N93f78a4e6d0265362062 is contained in Nd87b5f5caec8e6812340. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 38; delivered: 38; evidence tokens: 4096.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C6522cdd91136ea81cb55

Pair: **F20003** / partner **C8df4eb422ddda77c47ec**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N68253ce6d9b195c5dacc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Eed92e132a6420691c442` from `D4248752d2785e5bac1e0`: `N68253ce6d9b195c5dacc --NOT CONTAINED_IN--> Ncb8e73c65bdcc4819fa3`.

Canonical positive-chain target: `Ncc69027d69c243c0f5a9`. Denied object: `Ncb8e73c65bdcc4819fa3`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N68253ce6d9b195c5dacc --CONTAINED_IN [E510c678e2030565fc05c; Db4656d39a9d08594c964]--> N27a21b96b1491171f92c --CONTAINED_IN [E668516fa57e50e3cd88b; Dbb866ffea43863d04da8]--> Ncc69027d69c243c0f5a9
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Db4656d39a9d08594c964** — shortest-path support; assertion `E510c678e2030565fc05c`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `f9295c1af59f8baeefdc2d24069fb36779a6b5e55d586309cae815629df3a206`.

> N68253ce6d9b195c5dacc is contained in N27a21b96b1491171f92c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dbb866ffea43863d04da8** — shortest-path support; assertion `E668516fa57e50e3cd88b`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c0ca39561f8261ab9263bc0d8c9012c1038e3309fd8edf4476fa7eefbc02dbf3`.

> N27a21b96b1491171f92c is contained in Ncc69027d69c243c0f5a9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4248752d2785e5bac1e0** — explicit denial; assertion `Eed92e132a6420691c442`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `7e74dad3f855e7522e61d9a6762c3c7051d25b2a8e1190114aa8ee47bdc7b2bc`.

> N68253ce6d9b195c5dacc is not contained in Ncb8e73c65bdcc4819fa3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1960a17d8787a3b1cee** — unrelated distractor; assertion `E4d86338ce7247a29f4f4`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `e43f2536d7c19740fc04cddf41f66bc9a7a39196c313626825017daacf269f0f`.

> N93f78a4e6d0265362062 is contained in N099894cda8f2f6a2b5b2. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5e36db57ddaf9a79ea52** — unrelated distractor; assertion `Ecce47c2f80d249bbfde1`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `1e7742ae21de7409ad308b4090b9ecf478797233e174f546da54f4dee2baa35a`.

> N93f78a4e6d0265362062 is contained in Nd87b5f5caec8e6812340. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C4a7e4f1a97759d4e6cc0

Pair: **F20004** / partner **Cd65cb6bb1011932cfaaf**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N76575f0099b74a526d26? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E913ecd8fe833064ded8e` from `D5379b40bbb65d2149d75`: `N76575f0099b74a526d26 --NOT SUBREGION_OF--> N9005dee13ae53e890c51`.

Canonical positive-chain target: `N9005dee13ae53e890c51`. Denied object: `N9005dee13ae53e890c51`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N76575f0099b74a526d26 --SUBREGION_OF [E19536dcc1592a6db7fd4; Ddf4508c438a35f9493ca]--> Nd47b24f40ae4a0788925 --SUBREGION_OF [E1a12c126d0d81ab42fba; Dafb6461438342fc8247c]--> N9005dee13ae53e890c51
```

Conflict witness sets (support plus separate denial): `[["E19536dcc1592a6db7fd4","E1a12c126d0d81ab42fba","E913ecd8fe833064ded8e"]]`.

### Source documents (verbatim)

**Ddf4508c438a35f9493ca** — shortest-path support; assertion `E19536dcc1592a6db7fd4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `3968183193527420ea313eb1190a3ef5f4213fd0eb02ee7472102d5a2b6fb3df`.

> N76575f0099b74a526d26 is a subregion of Nd47b24f40ae4a0788925. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dafb6461438342fc8247c** — shortest-path support; assertion `E1a12c126d0d81ab42fba`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1021b25862abe992bc691977b0e114a52a4b064b3ce040ffd544e297e6c7590f`.

> Nd47b24f40ae4a0788925 is a subregion of N9005dee13ae53e890c51. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5379b40bbb65d2149d75** — explicit denial; assertion `E913ecd8fe833064ded8e`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `6be7584f65d38c6335349e29db599725307dd9f77da66b6d2024f8ee75c8df97`.

> N76575f0099b74a526d26 is not a subregion of N9005dee13ae53e890c51. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D32fee42740fc2d3298a6** — unrelated distractor; assertion `Ee3199e33ea70d9730f6c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `09f0cc88257a5e4daefc6e9f477a4a2e05c6acea7177a62b75a57ee0b5d12ab2`.

> N7e347bf05f241b885e0f is a subregion of N71582801d1189684c2be. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5bd8e791b5bd39d8bab0** — unrelated distractor; assertion `E9336976701711ea871c4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7533a97b53ca8e74642ca80b2b7a7e65a40a22d47e641b09798d4e375523083a`.

> N7e347bf05f241b885e0f is a subregion of N51b1f65ecb20100c0101. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 38; delivered: 38; evidence tokens: 4085.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cd65cb6bb1011932cfaaf

Pair: **F20004** / partner **C4a7e4f1a97759d4e6cc0**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N76575f0099b74a526d26? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ea5e8ca3bf42b05d73930` from `D9c01ceca580f57a3a888`: `N76575f0099b74a526d26 --NOT SUBREGION_OF--> Ne996765f9d28d4bbf636`.

Canonical positive-chain target: `N9005dee13ae53e890c51`. Denied object: `Ne996765f9d28d4bbf636`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N76575f0099b74a526d26 --SUBREGION_OF [E19536dcc1592a6db7fd4; Ddf4508c438a35f9493ca]--> Nd47b24f40ae4a0788925 --SUBREGION_OF [E1a12c126d0d81ab42fba; Dafb6461438342fc8247c]--> N9005dee13ae53e890c51
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Ddf4508c438a35f9493ca** — shortest-path support; assertion `E19536dcc1592a6db7fd4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `3968183193527420ea313eb1190a3ef5f4213fd0eb02ee7472102d5a2b6fb3df`.

> N76575f0099b74a526d26 is a subregion of Nd47b24f40ae4a0788925. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dafb6461438342fc8247c** — shortest-path support; assertion `E1a12c126d0d81ab42fba`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1021b25862abe992bc691977b0e114a52a4b064b3ce040ffd544e297e6c7590f`.

> Nd47b24f40ae4a0788925 is a subregion of N9005dee13ae53e890c51. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D9c01ceca580f57a3a888** — explicit denial; assertion `Ea5e8ca3bf42b05d73930`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `86c663f87175775749a620a28be59b81abfd03bfb09d3829aac778faddf7a5b2`.

> N76575f0099b74a526d26 is not a subregion of Ne996765f9d28d4bbf636. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D32fee42740fc2d3298a6** — unrelated distractor; assertion `Ee3199e33ea70d9730f6c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `09f0cc88257a5e4daefc6e9f477a4a2e05c6acea7177a62b75a57ee0b5d12ab2`.

> N7e347bf05f241b885e0f is a subregion of N71582801d1189684c2be. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5bd8e791b5bd39d8bab0** — unrelated distractor; assertion `E9336976701711ea871c4`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7533a97b53ca8e74642ca80b2b7a7e65a40a22d47e641b09798d4e375523083a`.

> N7e347bf05f241b885e0f is a subregion of N51b1f65ecb20100c0101. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4092.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C7ea35110eeccbbdc7dc9

Pair: **F20005** / partner **Cfa96317b5e41255c0ec2**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nb3157744fbca11401254? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E8c3bbaa28e4d304d0ab0` from `D213d059cbf8275626d71`: `Nb3157744fbca11401254 --NOT PRECEDES--> N9917c899684329d6eb7a`.

Canonical positive-chain target: `N9917c899684329d6eb7a`. Denied object: `N9917c899684329d6eb7a`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
Nb3157744fbca11401254 --PRECEDES [E2405a3f468bd6cba6e47; Df1b1e893965d3f189eb8]--> Na1d0dcf562bd43f98e5f --PRECEDES [Ee1dfd8a7a8c4e83351fc; De5d52bc41134b6f51dcf]--> N9917c899684329d6eb7a
```

Conflict witness sets (support plus separate denial): `[["E2405a3f468bd6cba6e47","E8c3bbaa28e4d304d0ab0","Ee1dfd8a7a8c4e83351fc"]]`.

### Source documents (verbatim)

**Df1b1e893965d3f189eb8** — shortest-path support; assertion `E2405a3f468bd6cba6e47`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `50e83c6170de23182e69caf2ae2250741b5b257d85e2aac0fba05702e3f61e8f`.

> Nb3157744fbca11401254 precedes Na1d0dcf562bd43f98e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De5d52bc41134b6f51dcf** — shortest-path support; assertion `Ee1dfd8a7a8c4e83351fc`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `23ef46e48025880e5046a5a98b171ec2de329908710dbfbfe3dbdd4bf2840f73`.

> Na1d0dcf562bd43f98e5f precedes N9917c899684329d6eb7a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D213d059cbf8275626d71** — explicit denial; assertion `E8c3bbaa28e4d304d0ab0`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `b345b784eb59a1dc756cd24cc42a8e4d3007709764e37ae18721edae76323b75`.

> Nb3157744fbca11401254 does not precede N9917c899684329d6eb7a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De6504e4466c5e590a4d1** — unrelated distractor; assertion `Ecf22fbf5d3a34bf53fa3`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `6f09ace2b67faf18bb3304206f6cff6f922ec8625ec245cb5695aea6fc7352e5`.

> N2d03a1f82ddd8c26d2d9 precedes Nca4b0e1cb75f547231b1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2a2fa858c97ab6d6fbdc** — unrelated distractor; assertion `E49c35a33f12172c92eff`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `2ce9f26fdaf765ff9b5385e5fd68b1f571baee7a3facce2dcbef1e960dc0f7af`.

> N2d03a1f82ddd8c26d2d9 precedes N4ac05f63fb6dd5f25107. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 38; delivered: 38; evidence tokens: 4089.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cfa96317b5e41255c0ec2

Pair: **F20005** / partner **C7ea35110eeccbbdc7dc9**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nb3157744fbca11401254? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Edd6cf52bbe2c81ed78de` from `D6bc36a09c6ec8f5132fb`: `Nb3157744fbca11401254 --NOT PRECEDES--> N41038840007d9a7d4f12`.

Canonical positive-chain target: `N9917c899684329d6eb7a`. Denied object: `N41038840007d9a7d4f12`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
Nb3157744fbca11401254 --PRECEDES [E2405a3f468bd6cba6e47; Df1b1e893965d3f189eb8]--> Na1d0dcf562bd43f98e5f --PRECEDES [Ee1dfd8a7a8c4e83351fc; De5d52bc41134b6f51dcf]--> N9917c899684329d6eb7a
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Df1b1e893965d3f189eb8** — shortest-path support; assertion `E2405a3f468bd6cba6e47`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `50e83c6170de23182e69caf2ae2250741b5b257d85e2aac0fba05702e3f61e8f`.

> Nb3157744fbca11401254 precedes Na1d0dcf562bd43f98e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De5d52bc41134b6f51dcf** — shortest-path support; assertion `Ee1dfd8a7a8c4e83351fc`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `23ef46e48025880e5046a5a98b171ec2de329908710dbfbfe3dbdd4bf2840f73`.

> Na1d0dcf562bd43f98e5f precedes N9917c899684329d6eb7a. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6bc36a09c6ec8f5132fb** — explicit denial; assertion `Edd6cf52bbe2c81ed78de`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `3f26b557b9496ecd0c449d9ab0a151fe7c32ac6efc4c935896a8ca405a0dff4a`.

> Nb3157744fbca11401254 does not precede N41038840007d9a7d4f12. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De6504e4466c5e590a4d1** — unrelated distractor; assertion `Ecf22fbf5d3a34bf53fa3`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `6f09ace2b67faf18bb3304206f6cff6f922ec8625ec245cb5695aea6fc7352e5`.

> N2d03a1f82ddd8c26d2d9 precedes Nca4b0e1cb75f547231b1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2a2fa858c97ab6d6fbdc** — unrelated distractor; assertion `E49c35a33f12172c92eff`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `2ce9f26fdaf765ff9b5385e5fd68b1f571baee7a3facce2dcbef1e960dc0f7af`.

> N2d03a1f82ddd8c26d2d9 precedes N4ac05f63fb6dd5f25107. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 32; delivered: 32; evidence tokens: 4080.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Ca5cf3e75e3d2fddf1810

Pair: **F20006** / partner **Cce7e332b5c6ca12c3659**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N95fb109be72efd322e6f? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E9bb94c58a712a294c5e4` from `Dbafebf997bd9cd9d8308`: `N95fb109be72efd322e6f --NOT CONTAINED_IN--> Nc91a8abe309bcd9c0856`.

Canonical positive-chain target: `Nc91a8abe309bcd9c0856`. Denied object: `Nc91a8abe309bcd9c0856`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N95fb109be72efd322e6f --CONTAINED_IN [E764d4d8b5a430aad5bbd; Deaad463ce80c534b1f76]--> N9a427e3874430f8172ef --CONTAINED_IN [E0fd0a1d330b69a1064cf; D00acb34e9b7189e2447a]--> Nc91a8abe309bcd9c0856
```

Conflict witness sets (support plus separate denial): `[["E0fd0a1d330b69a1064cf","E764d4d8b5a430aad5bbd","E9bb94c58a712a294c5e4"]]`.

### Source documents (verbatim)

**Deaad463ce80c534b1f76** — shortest-path support; assertion `E764d4d8b5a430aad5bbd`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `b5b6f1834fa03c6b32174a089197e6830c8f773a3c15f6a2e5f478dc2f259491`.

> N95fb109be72efd322e6f is contained in N9a427e3874430f8172ef. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D00acb34e9b7189e2447a** — shortest-path support; assertion `E0fd0a1d330b69a1064cf`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `51f53122b28c87d0fd79f37a5c6d0cb3d442aca1ce7cdc140734c7a00b9d3a80`.

> N9a427e3874430f8172ef is contained in Nc91a8abe309bcd9c0856. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dbafebf997bd9cd9d8308** — explicit denial; assertion `E9bb94c58a712a294c5e4`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `0923547d16505fa085d352085095f88e6b0297e381431cc725ece92576400db6`.

> N95fb109be72efd322e6f is not contained in Nc91a8abe309bcd9c0856. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D8c8029e8c48a14776585** — unrelated distractor; assertion `E0816b844241bd605e98c`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `cdc54ab6bd34689366c1037fdf3236c75253f4a17f37b9d6f21db696d213c4ca`.

> N78393c88903f75efa53e is contained in N9c09fa856f253442f548. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D999f35a71e98b3acc633** — unrelated distractor; assertion `Ed6481fe28a04690cc24f`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `729ae220dc43d2560a58ebb0dc0e5d004cf7037fe4a1c2c214cc374774058de9`.

> N78393c88903f75efa53e is contained in N276de54cc68d39328341. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 39; delivered: 39; evidence tokens: 4084.

Missing witness assertions before budget: `[["E0fd0a1d330b69a1064cf"]]`; after budget: `[["E0fd0a1d330b69a1064cf"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cce7e332b5c6ca12c3659

Pair: **F20006** / partner **Ca5cf3e75e3d2fddf1810**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N95fb109be72efd322e6f? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ebd590dac41c53df6dfdf` from `D1c2b0ba00cb00e9e9db2`: `N95fb109be72efd322e6f --NOT CONTAINED_IN--> N064c85e84aa99dbbf6d9`.

Canonical positive-chain target: `Nc91a8abe309bcd9c0856`. Denied object: `N064c85e84aa99dbbf6d9`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N95fb109be72efd322e6f --CONTAINED_IN [E764d4d8b5a430aad5bbd; Deaad463ce80c534b1f76]--> N9a427e3874430f8172ef --CONTAINED_IN [E0fd0a1d330b69a1064cf; D00acb34e9b7189e2447a]--> Nc91a8abe309bcd9c0856
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Deaad463ce80c534b1f76** — shortest-path support; assertion `E764d4d8b5a430aad5bbd`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `b5b6f1834fa03c6b32174a089197e6830c8f773a3c15f6a2e5f478dc2f259491`.

> N95fb109be72efd322e6f is contained in N9a427e3874430f8172ef. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D00acb34e9b7189e2447a** — shortest-path support; assertion `E0fd0a1d330b69a1064cf`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `51f53122b28c87d0fd79f37a5c6d0cb3d442aca1ce7cdc140734c7a00b9d3a80`.

> N9a427e3874430f8172ef is contained in Nc91a8abe309bcd9c0856. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D1c2b0ba00cb00e9e9db2** — explicit denial; assertion `Ebd590dac41c53df6dfdf`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `230b3645aad3d66a53c4b4769f5ae9e2b8bc4859ce5140d58bacc55cc5e6a03b`.

> N95fb109be72efd322e6f is not contained in N064c85e84aa99dbbf6d9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D8c8029e8c48a14776585** — unrelated distractor; assertion `E0816b844241bd605e98c`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `cdc54ab6bd34689366c1037fdf3236c75253f4a17f37b9d6f21db696d213c4ca`.

> N78393c88903f75efa53e is contained in N9c09fa856f253442f548. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D999f35a71e98b3acc633** — unrelated distractor; assertion `Ed6481fe28a04690cc24f`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `729ae220dc43d2560a58ebb0dc0e5d004cf7037fe4a1c2c214cc374774058de9`.

> N78393c88903f75efa53e is contained in N276de54cc68d39328341. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4084.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cd4415c7ca842d8437c46

Pair: **F20007** / partner **C4f22a075bbaa8c11d46e**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N9932b69591573a3c46d1? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ec660bdbf3c39e5b3e5d0` from `D606ed73f3866f2e4f0d1`: `N9932b69591573a3c46d1 --NOT SUBREGION_OF--> Nf2d2929a65de8c7aae4c`.

Canonical positive-chain target: `Nf2d2929a65de8c7aae4c`. Denied object: `Nf2d2929a65de8c7aae4c`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N9932b69591573a3c46d1 --SUBREGION_OF [E9342c48404dcfe5db9bf; D9f759ab27061c634112b]--> N90de20f96ad7dc946afb --SUBREGION_OF [Ead7f5f4ff1e53f40bdf0; D31d7efaecc9dac0459f5]--> Nf2d2929a65de8c7aae4c
```

Conflict witness sets (support plus separate denial): `[["E9342c48404dcfe5db9bf","Ead7f5f4ff1e53f40bdf0","Ec660bdbf3c39e5b3e5d0"]]`.

### Source documents (verbatim)

**D9f759ab27061c634112b** — shortest-path support; assertion `E9342c48404dcfe5db9bf`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `47b4586e1167901f14fe037da04fb1c65e6006910f6cbd2e5f5100a6022b843c`.

> N9932b69591573a3c46d1 is a subregion of N90de20f96ad7dc946afb. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D31d7efaecc9dac0459f5** — shortest-path support; assertion `Ead7f5f4ff1e53f40bdf0`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2763610b923c7d1b3ecbfad48d1ab3c794546402992fb92c519d103c5a56804f`.

> N90de20f96ad7dc946afb is a subregion of Nf2d2929a65de8c7aae4c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D606ed73f3866f2e4f0d1** — explicit denial; assertion `Ec660bdbf3c39e5b3e5d0`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `bcacf36a707b6e2ed13b0889c7f2ab75fdc2c5aa2c23eb91d90c5a4e40d4fe26`.

> N9932b69591573a3c46d1 is not a subregion of Nf2d2929a65de8c7aae4c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6bb1b6280699474cd4da** — unrelated distractor; assertion `E478993905fd0164a2389`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `d4f5d4c8f9f919abaca11fee465165be6b1a1e7102c1d14989c5626b83e7bfd0`.

> N9f8e15093ef70a5dad32 is a subregion of N85b67e18c541fe99adfa. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D69ab7fa586361d0bba4c** — unrelated distractor; assertion `E20b763ebab32703d5efd`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7101859a9c7c9cc4d9ead23072d35272b798fc2d16366cb3995b274865256ad1`.

> N9f8e15093ef70a5dad32 is a subregion of Ne355e96ee6408c2dd382. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4095.

Missing witness assertions before budget: `[["Ead7f5f4ff1e53f40bdf0"]]`; after budget: `[["Ead7f5f4ff1e53f40bdf0"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C4f22a075bbaa8c11d46e

Pair: **F20007** / partner **Cd4415c7ca842d8437c46**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **2**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N9932b69591573a3c46d1? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E890766a94baa5358e940` from `Df9338c880fc02079ed14`: `N9932b69591573a3c46d1 --NOT SUBREGION_OF--> N2311a6096f1d25547008`.

Canonical positive-chain target: `Nf2d2929a65de8c7aae4c`. Denied object: `N2311a6096f1d25547008`.

### All shortest positive source-backed paths

Path 1 (2 supporting hops):

```text
N9932b69591573a3c46d1 --SUBREGION_OF [E9342c48404dcfe5db9bf; D9f759ab27061c634112b]--> N90de20f96ad7dc946afb --SUBREGION_OF [Ead7f5f4ff1e53f40bdf0; D31d7efaecc9dac0459f5]--> Nf2d2929a65de8c7aae4c
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D9f759ab27061c634112b** — shortest-path support; assertion `E9342c48404dcfe5db9bf`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `47b4586e1167901f14fe037da04fb1c65e6006910f6cbd2e5f5100a6022b843c`.

> N9932b69591573a3c46d1 is a subregion of N90de20f96ad7dc946afb. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D31d7efaecc9dac0459f5** — shortest-path support; assertion `Ead7f5f4ff1e53f40bdf0`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `2763610b923c7d1b3ecbfad48d1ab3c794546402992fb92c519d103c5a56804f`.

> N90de20f96ad7dc946afb is a subregion of Nf2d2929a65de8c7aae4c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df9338c880fc02079ed14** — explicit denial; assertion `E890766a94baa5358e940`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `0c78e9229d6a19320ec8be280ae59b0f109e688f1fe1daa2ba3929c0068b7665`.

> N9932b69591573a3c46d1 is not a subregion of N2311a6096f1d25547008. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6bb1b6280699474cd4da** — unrelated distractor; assertion `E478993905fd0164a2389`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `d4f5d4c8f9f919abaca11fee465165be6b1a1e7102c1d14989c5626b83e7bfd0`.

> N9f8e15093ef70a5dad32 is a subregion of N85b67e18c541fe99adfa. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D69ab7fa586361d0bba4c** — unrelated distractor; assertion `E20b763ebab32703d5efd`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7101859a9c7c9cc4d9ead23072d35272b798fc2d16366cb3995b274865256ad1`.

> N9f8e15093ef70a5dad32 is a subregion of Ne355e96ee6408c2dd382. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 32; delivered: 32; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C9ad27ae96d1771959b51

Pair: **F30000** / partner **C867476b9eda45605182a**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N65700a2d6db36d25598a? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E837eb7fd6f1d87eb594b` from `D42a6ad15e475e77a44ea`: `N65700a2d6db36d25598a --NOT CONTAINED_IN--> N5df6c26f99d2dabea078`.

Canonical positive-chain target: `N5df6c26f99d2dabea078`. Denied object: `N5df6c26f99d2dabea078`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N65700a2d6db36d25598a --CONTAINED_IN [Ecabbeafede29ec5a2b96; D3369302a126998523134]--> N4f8b6237641fd828e3d1 --CONTAINED_IN [Ea46ceeb6284181742429; D810fe8668f225c16c82c]--> N5fce270295be035aa745 --CONTAINED_IN [E60ac2b434d56c4db1105; D6d1b7dca231782eb5c7f]--> N5df6c26f99d2dabea078
```

Conflict witness sets (support plus separate denial): `[["E60ac2b434d56c4db1105","E837eb7fd6f1d87eb594b","Ea46ceeb6284181742429","Ecabbeafede29ec5a2b96"]]`.

### Source documents (verbatim)

**D3369302a126998523134** — shortest-path support; assertion `Ecabbeafede29ec5a2b96`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `913ce2b6aa1770581de2ffb47f245d326a2de68075063f4fe9aea9bcd0ae1bc1`.

> N65700a2d6db36d25598a is contained in N4f8b6237641fd828e3d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D810fe8668f225c16c82c** — shortest-path support; assertion `Ea46ceeb6284181742429`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `619a87b254765cfcb86103863869fe25f16d2e4720599d0671a803bb9db1b1c5`.

> N4f8b6237641fd828e3d1 is contained in N5fce270295be035aa745. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6d1b7dca231782eb5c7f** — shortest-path support; assertion `E60ac2b434d56c4db1105`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `6f12c3e09141271f852b94e5edfff11fbffc413a87235836dc94d3dc2dea5305`.

> N5fce270295be035aa745 is contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D42a6ad15e475e77a44ea** — explicit denial; assertion `E837eb7fd6f1d87eb594b`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `3deeba0659b642cf762d8a3da8383aed0756bbc5a4afe076a7dde79f186d0139`.

> N65700a2d6db36d25598a is not contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D92b87fb4dd790a9a0f2f** — unrelated distractor; assertion `E6111ec133352d4c2cbfd`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `45e22026481a8317603a7bc5364697be60c34a124a0a003d08e92cb25398220c`.

> Ncbbbb26b53e20af47e6d is contained in N53ae6479da267416f91d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4028633f7f07194a89fc** — unrelated distractor; assertion `E69941b27b59a96c45cd4`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `4daa8ebf27deea7bb90ee7ab9f9eafe6b42ec44caac67df7c9ee2cd1ef1b0f39`.

> Ncbbbb26b53e20af47e6d is contained in N608c6ed4328ab6d8bf66. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4089.

Missing witness assertions before budget: `[["E60ac2b434d56c4db1105","Ea46ceeb6284181742429"]]`; after budget: `[["E60ac2b434d56c4db1105","Ea46ceeb6284181742429"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C867476b9eda45605182a

Pair: **F30000** / partner **C9ad27ae96d1771959b51**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N65700a2d6db36d25598a? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E248e1076a3c85d72abcb` from `D112f091f348d72661fce`: `N65700a2d6db36d25598a --NOT CONTAINED_IN--> N0fa75f761a41530bd9d4`.

Canonical positive-chain target: `N5df6c26f99d2dabea078`. Denied object: `N0fa75f761a41530bd9d4`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N65700a2d6db36d25598a --CONTAINED_IN [Ecabbeafede29ec5a2b96; D3369302a126998523134]--> N4f8b6237641fd828e3d1 --CONTAINED_IN [Ea46ceeb6284181742429; D810fe8668f225c16c82c]--> N5fce270295be035aa745 --CONTAINED_IN [E60ac2b434d56c4db1105; D6d1b7dca231782eb5c7f]--> N5df6c26f99d2dabea078
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D3369302a126998523134** — shortest-path support; assertion `Ecabbeafede29ec5a2b96`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `913ce2b6aa1770581de2ffb47f245d326a2de68075063f4fe9aea9bcd0ae1bc1`.

> N65700a2d6db36d25598a is contained in N4f8b6237641fd828e3d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D810fe8668f225c16c82c** — shortest-path support; assertion `Ea46ceeb6284181742429`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `619a87b254765cfcb86103863869fe25f16d2e4720599d0671a803bb9db1b1c5`.

> N4f8b6237641fd828e3d1 is contained in N5fce270295be035aa745. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6d1b7dca231782eb5c7f** — shortest-path support; assertion `E60ac2b434d56c4db1105`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `6f12c3e09141271f852b94e5edfff11fbffc413a87235836dc94d3dc2dea5305`.

> N5fce270295be035aa745 is contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D112f091f348d72661fce** — explicit denial; assertion `E248e1076a3c85d72abcb`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `d90accedee516f1d9210205665ffa7d22b5c8d4585337b34ede6c0b5ac6520dc`.

> N65700a2d6db36d25598a is not contained in N0fa75f761a41530bd9d4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D92b87fb4dd790a9a0f2f** — unrelated distractor; assertion `E6111ec133352d4c2cbfd`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `45e22026481a8317603a7bc5364697be60c34a124a0a003d08e92cb25398220c`.

> Ncbbbb26b53e20af47e6d is contained in N53ae6479da267416f91d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4028633f7f07194a89fc** — unrelated distractor; assertion `E69941b27b59a96c45cd4`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `4daa8ebf27deea7bb90ee7ab9f9eafe6b42ec44caac67df7c9ee2cd1ef1b0f39`.

> Ncbbbb26b53e20af47e6d is contained in N608c6ed4328ab6d8bf66. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4091.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C18c3b347fd4b60f07d70

Pair: **F30001** / partner **C72bd1b5ee97f58f77f35**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N8fe9e9640a4262cfd99d? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Efe0998561ce841c0cadc` from `D0b3092068b267ade7047`: `N8fe9e9640a4262cfd99d --NOT SUBREGION_OF--> N6a09c8b2f74d7ae96dd7`.

Canonical positive-chain target: `N6a09c8b2f74d7ae96dd7`. Denied object: `N6a09c8b2f74d7ae96dd7`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N8fe9e9640a4262cfd99d --SUBREGION_OF [E91a0ef8313a036fbf60e; Df9188b96fa8391566057]--> N6c8a83ea31d62164b287 --SUBREGION_OF [E570c5a8715a0c2da81da; D84639360e642b7f63859]--> N4d25d1380a1dc3194e5f --SUBREGION_OF [Edb8e57de3f5ac8e94f65; D3de38f34fc4fd8208986]--> N6a09c8b2f74d7ae96dd7
```

Conflict witness sets (support plus separate denial): `[["E570c5a8715a0c2da81da","E91a0ef8313a036fbf60e","Edb8e57de3f5ac8e94f65","Efe0998561ce841c0cadc"]]`.

### Source documents (verbatim)

**Df9188b96fa8391566057** — shortest-path support; assertion `E91a0ef8313a036fbf60e`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7c03b9d82fa7001eddf5d0ca17f7b7a72bfc05bac86995bb0a7d4059239e4da9`.

> N8fe9e9640a4262cfd99d is a subregion of N6c8a83ea31d62164b287. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D84639360e642b7f63859** — shortest-path support; assertion `E570c5a8715a0c2da81da`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a758d723e75aaa5c5252bf7f39ada35665b7b5d100e47b79a8d4bd1e1f4766e7`.

> N6c8a83ea31d62164b287 is a subregion of N4d25d1380a1dc3194e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3de38f34fc4fd8208986** — shortest-path support; assertion `Edb8e57de3f5ac8e94f65`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `ac8fa6ed13296c5820c6df41079dc0a43c43fc9f0d4e0c6d097fc33089e90ad8`.

> N4d25d1380a1dc3194e5f is a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D0b3092068b267ade7047** — explicit denial; assertion `Efe0998561ce841c0cadc`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `901d67db58e126a0219b79d63a018f8b42c4dd2a88d42a98bcdf8fca9fe990cf`.

> N8fe9e9640a4262cfd99d is not a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3bf755801edbd55b30c7** — unrelated distractor; assertion `Eac7ca624fbad60342656`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1dabb1a385c891fc06597ade9ed321b81b5de86fb95e2654c604ed214193e34a`.

> Nf2b79bb0ae62811bda41 is a subregion of N1ccedfeba71398b7cdb9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1b71a1b0a096adfd662** — unrelated distractor; assertion `E180f4f08d566c5c09dc6`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `64aa1c49e66e28d07d07113bf5dd52210c7e84e177b6d31ac1afe0ec1f1ed259`.

> Nf2b79bb0ae62811bda41 is a subregion of Nb41ba5e6f39521b6e691. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4093.

Missing witness assertions before budget: `[["E570c5a8715a0c2da81da","Edb8e57de3f5ac8e94f65"]]`; after budget: `[["E570c5a8715a0c2da81da","Edb8e57de3f5ac8e94f65"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C72bd1b5ee97f58f77f35

Pair: **F30001** / partner **C18c3b347fd4b60f07d70**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N8fe9e9640a4262cfd99d? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E138b172bc81a8b1ab899` from `Db050aa36b577efe8b565`: `N8fe9e9640a4262cfd99d --NOT SUBREGION_OF--> Ne0c5ea0e185fd8d3c041`.

Canonical positive-chain target: `N6a09c8b2f74d7ae96dd7`. Denied object: `Ne0c5ea0e185fd8d3c041`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N8fe9e9640a4262cfd99d --SUBREGION_OF [E91a0ef8313a036fbf60e; Df9188b96fa8391566057]--> N6c8a83ea31d62164b287 --SUBREGION_OF [E570c5a8715a0c2da81da; D84639360e642b7f63859]--> N4d25d1380a1dc3194e5f --SUBREGION_OF [Edb8e57de3f5ac8e94f65; D3de38f34fc4fd8208986]--> N6a09c8b2f74d7ae96dd7
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Df9188b96fa8391566057** — shortest-path support; assertion `E91a0ef8313a036fbf60e`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `7c03b9d82fa7001eddf5d0ca17f7b7a72bfc05bac86995bb0a7d4059239e4da9`.

> N8fe9e9640a4262cfd99d is a subregion of N6c8a83ea31d62164b287. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D84639360e642b7f63859** — shortest-path support; assertion `E570c5a8715a0c2da81da`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `a758d723e75aaa5c5252bf7f39ada35665b7b5d100e47b79a8d4bd1e1f4766e7`.

> N6c8a83ea31d62164b287 is a subregion of N4d25d1380a1dc3194e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3de38f34fc4fd8208986** — shortest-path support; assertion `Edb8e57de3f5ac8e94f65`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `ac8fa6ed13296c5820c6df41079dc0a43c43fc9f0d4e0c6d097fc33089e90ad8`.

> N4d25d1380a1dc3194e5f is a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db050aa36b577efe8b565** — explicit denial; assertion `E138b172bc81a8b1ab899`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `742e4917158b3a3359cb2ea6e0d46d41eea4779de27e7a0ade7463cc5fbadc5d`.

> N8fe9e9640a4262cfd99d is not a subregion of Ne0c5ea0e185fd8d3c041. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3bf755801edbd55b30c7** — unrelated distractor; assertion `Eac7ca624fbad60342656`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1dabb1a385c891fc06597ade9ed321b81b5de86fb95e2654c604ed214193e34a`.

> Nf2b79bb0ae62811bda41 is a subregion of N1ccedfeba71398b7cdb9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1b71a1b0a096adfd662** — unrelated distractor; assertion `E180f4f08d566c5c09dc6`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `64aa1c49e66e28d07d07113bf5dd52210c7e84e177b6d31ac1afe0ec1f1ed259`.

> Nf2b79bb0ae62811bda41 is a subregion of Nb41ba5e6f39521b6e691. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4090.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C45e88caf1e8b13cac59e

Pair: **F30002** / partner **Ca13cd3fae860c8b5fd24**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nf96405a2392fdff9bb1e? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ee6e68b56d920713b48aa` from `D29a62f45335d85618f92`: `Nf96405a2392fdff9bb1e --NOT PRECEDES--> N0281ead2d0c61309aff9`.

Canonical positive-chain target: `N0281ead2d0c61309aff9`. Denied object: `N0281ead2d0c61309aff9`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
Nf96405a2392fdff9bb1e --PRECEDES [E2ece4a4480441f242b4d; De225409809272256bf02]--> N59c527434fc54854dad3 --PRECEDES [E22b4c4719f980d27c947; D00aa2f4b14fa5e79bf07]--> N30a734839dd9c6a7787f --PRECEDES [E2eb9eaf480db10d10579; Dfdad841b91e6356bb92d]--> N0281ead2d0c61309aff9
```

Conflict witness sets (support plus separate denial): `[["E22b4c4719f980d27c947","E2eb9eaf480db10d10579","E2ece4a4480441f242b4d","Ee6e68b56d920713b48aa"]]`.

### Source documents (verbatim)

**De225409809272256bf02** — shortest-path support; assertion `E2ece4a4480441f242b4d`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `21db5e09f13c1166f7d68bc98eb7cabd79ade00a6a0d99b00a1bdd0a8b917095`.

> Nf96405a2392fdff9bb1e precedes N59c527434fc54854dad3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D00aa2f4b14fa5e79bf07** — shortest-path support; assertion `E22b4c4719f980d27c947`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `e855548706e7ef01c6c3959f124966f94d4a662b4483f12f88b3dcc95579ab2d`.

> N59c527434fc54854dad3 precedes N30a734839dd9c6a7787f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfdad841b91e6356bb92d** — shortest-path support; assertion `E2eb9eaf480db10d10579`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `0de3591ea9d7de74dae6d321c63abe74444d6c3eb4436bd43cc0044a2d954143`.

> N30a734839dd9c6a7787f precedes N0281ead2d0c61309aff9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D29a62f45335d85618f92** — explicit denial; assertion `Ee6e68b56d920713b48aa`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `c12b105a013b320c35963324cd301c5630ca2de4e7e69516f0935d7ed2390214`.

> Nf96405a2392fdff9bb1e does not precede N0281ead2d0c61309aff9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D580955e60cfcced500f1** — unrelated distractor; assertion `Eef2576d0afd55887432a`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `ca2bcdec8b1327e6bffc400f70d3f293eda9a1660c2d31070eef036714c167a0`.

> N50a946b25b186c5bc4a1 precedes N3348662b17667059bb08. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6af3230e4a34d9d96ade** — unrelated distractor; assertion `Ea78201ca30ac6698cc1e`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `64a6a7374d66599061eea915ed2fb89c24470083e108c235cc7da8531df582ff`.

> N50a946b25b186c5bc4a1 precedes N75c4a51de4e9bc2ba616. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tp**; failure: **none**. Raw source chunks: 37; delivered: 37; evidence tokens: 4091.

Missing witness assertions before budget: `[[]]`; after budget: `[[]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Ca13cd3fae860c8b5fd24

Pair: **F30002** / partner **C45e88caf1e8b13cac59e**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nf96405a2392fdff9bb1e? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E2a2891579f6e1307a206` from `D25fbde5780c9df0a16a1`: `Nf96405a2392fdff9bb1e --NOT PRECEDES--> Nbf627d31a588c1259d80`.

Canonical positive-chain target: `N0281ead2d0c61309aff9`. Denied object: `Nbf627d31a588c1259d80`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
Nf96405a2392fdff9bb1e --PRECEDES [E2ece4a4480441f242b4d; De225409809272256bf02]--> N59c527434fc54854dad3 --PRECEDES [E22b4c4719f980d27c947; D00aa2f4b14fa5e79bf07]--> N30a734839dd9c6a7787f --PRECEDES [E2eb9eaf480db10d10579; Dfdad841b91e6356bb92d]--> N0281ead2d0c61309aff9
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**De225409809272256bf02** — shortest-path support; assertion `E2ece4a4480441f242b4d`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `21db5e09f13c1166f7d68bc98eb7cabd79ade00a6a0d99b00a1bdd0a8b917095`.

> Nf96405a2392fdff9bb1e precedes N59c527434fc54854dad3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D00aa2f4b14fa5e79bf07** — shortest-path support; assertion `E22b4c4719f980d27c947`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `e855548706e7ef01c6c3959f124966f94d4a662b4483f12f88b3dcc95579ab2d`.

> N59c527434fc54854dad3 precedes N30a734839dd9c6a7787f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfdad841b91e6356bb92d** — shortest-path support; assertion `E2eb9eaf480db10d10579`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `0de3591ea9d7de74dae6d321c63abe74444d6c3eb4436bd43cc0044a2d954143`.

> N30a734839dd9c6a7787f precedes N0281ead2d0c61309aff9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D25fbde5780c9df0a16a1** — explicit denial; assertion `E2a2891579f6e1307a206`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `0384def9153e2ee7cb1c968ab9f8cb010357154425ba870acd445300a74c42f9`.

> Nf96405a2392fdff9bb1e does not precede Nbf627d31a588c1259d80. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D580955e60cfcced500f1** — unrelated distractor; assertion `Eef2576d0afd55887432a`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `ca2bcdec8b1327e6bffc400f70d3f293eda9a1660c2d31070eef036714c167a0`.

> N50a946b25b186c5bc4a1 precedes N3348662b17667059bb08. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6af3230e4a34d9d96ade** — unrelated distractor; assertion `Ea78201ca30ac6698cc1e`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `64a6a7374d66599061eea915ed2fb89c24470083e108c235cc7da8531df582ff`.

> N50a946b25b186c5bc4a1 precedes N75c4a51de4e9bc2ba616. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 33; delivered: 33; evidence tokens: 4092.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C588987f4cc3505b4717d

Pair: **F30003** / partner **Cda357462e04448e2e7f8**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N250f79801241d60703ac? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ea4f0019192d800ed0ad2` from `D51c37d21d0db8f1e9c74`: `N250f79801241d60703ac --NOT CONTAINED_IN--> Nba3a0b991db4fb79cf0f`.

Canonical positive-chain target: `Nba3a0b991db4fb79cf0f`. Denied object: `Nba3a0b991db4fb79cf0f`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N250f79801241d60703ac --CONTAINED_IN [E19daf820545efa859bae; D47c49cfab181f97b6a71]--> N56eb25a25d389374758f --CONTAINED_IN [E49558aaa8558acadaee6; Db384c386a21952382238]--> Ne6ddd40967a46112c8b9 --CONTAINED_IN [Ec471bdd989cd33fcd65a; D28f16cd7a54c385b69ca]--> Nba3a0b991db4fb79cf0f
```

Conflict witness sets (support plus separate denial): `[["E19daf820545efa859bae","E49558aaa8558acadaee6","Ea4f0019192d800ed0ad2","Ec471bdd989cd33fcd65a"]]`.

### Source documents (verbatim)

**D47c49cfab181f97b6a71** — shortest-path support; assertion `E19daf820545efa859bae`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `0a58eddcdb7138b42952a8496bac908faee17307974569f39dd204fe263f817c`.

> N250f79801241d60703ac is contained in N56eb25a25d389374758f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db384c386a21952382238** — shortest-path support; assertion `E49558aaa8558acadaee6`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `5b3928c2a7ea6f62fb081bd37fd5d435fe65b2c047674f5ea427c219389918f3`.

> N56eb25a25d389374758f is contained in Ne6ddd40967a46112c8b9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D28f16cd7a54c385b69ca** — shortest-path support; assertion `Ec471bdd989cd33fcd65a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `af4bd498c70b4d75907150e987ca7ddac82d92813a9b5e7ab46c9968fa8109f8`.

> Ne6ddd40967a46112c8b9 is contained in Nba3a0b991db4fb79cf0f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D51c37d21d0db8f1e9c74** — explicit denial; assertion `Ea4f0019192d800ed0ad2`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `289f5e2bf90b8766e08adf050084556f91e2a2ec257dc95a704fb4ce258554f0`.

> N250f79801241d60703ac is not contained in Nba3a0b991db4fb79cf0f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4fecc98249c4af1af3ad** — unrelated distractor; assertion `Eef9cdb5968d1e437115d`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c1452e72b98d943e30ceb604168dede60f44119061e59107be796ed0a6545040`.

> Nc86b9a88c224130195ad is contained in N14289eaa346fdf8e2037. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D340ca21d12f63d1cd917** — unrelated distractor; assertion `E0220244d847302e14dee`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `d0391df3c1ba30be3b4917e510a3180b38eb0bb756fe2a0fd5270257cc73c6b9`.

> Nc86b9a88c224130195ad is contained in Na446443ea668d6e1e6e7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 39; delivered: 39; evidence tokens: 4085.

Missing witness assertions before budget: `[["Ec471bdd989cd33fcd65a"]]`; after budget: `[["Ec471bdd989cd33fcd65a"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cda357462e04448e2e7f8

Pair: **F30003** / partner **C588987f4cc3505b4717d**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N250f79801241d60703ac? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ed56d3ae4a69c2e2aaa70` from `Dac6853294564293d1c04`: `N250f79801241d60703ac --NOT CONTAINED_IN--> Nc2c7892d02eb5c71342e`.

Canonical positive-chain target: `Nba3a0b991db4fb79cf0f`. Denied object: `Nc2c7892d02eb5c71342e`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N250f79801241d60703ac --CONTAINED_IN [E19daf820545efa859bae; D47c49cfab181f97b6a71]--> N56eb25a25d389374758f --CONTAINED_IN [E49558aaa8558acadaee6; Db384c386a21952382238]--> Ne6ddd40967a46112c8b9 --CONTAINED_IN [Ec471bdd989cd33fcd65a; D28f16cd7a54c385b69ca]--> Nba3a0b991db4fb79cf0f
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D47c49cfab181f97b6a71** — shortest-path support; assertion `E19daf820545efa859bae`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `0a58eddcdb7138b42952a8496bac908faee17307974569f39dd204fe263f817c`.

> N250f79801241d60703ac is contained in N56eb25a25d389374758f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db384c386a21952382238** — shortest-path support; assertion `E49558aaa8558acadaee6`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `5b3928c2a7ea6f62fb081bd37fd5d435fe65b2c047674f5ea427c219389918f3`.

> N56eb25a25d389374758f is contained in Ne6ddd40967a46112c8b9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D28f16cd7a54c385b69ca** — shortest-path support; assertion `Ec471bdd989cd33fcd65a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `af4bd498c70b4d75907150e987ca7ddac82d92813a9b5e7ab46c9968fa8109f8`.

> Ne6ddd40967a46112c8b9 is contained in Nba3a0b991db4fb79cf0f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dac6853294564293d1c04** — explicit denial; assertion `Ed56d3ae4a69c2e2aaa70`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `689de70093cb928789072d9f307ab7dfeb2eea23ce6bcdf461196d0d97581df4`.

> N250f79801241d60703ac is not contained in Nc2c7892d02eb5c71342e. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4fecc98249c4af1af3ad** — unrelated distractor; assertion `Eef9cdb5968d1e437115d`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `c1452e72b98d943e30ceb604168dede60f44119061e59107be796ed0a6545040`.

> Nc86b9a88c224130195ad is contained in N14289eaa346fdf8e2037. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D340ca21d12f63d1cd917** — unrelated distractor; assertion `E0220244d847302e14dee`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `d0391df3c1ba30be3b4917e510a3180b38eb0bb756fe2a0fd5270257cc73c6b9`.

> Nc86b9a88c224130195ad is contained in Na446443ea668d6e1e6e7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4095.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## Cd232869ea3c6d7941431

Pair: **F30004** / partner **C8b19850343875fd938d3**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N6da7f19259247dae36bf? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ed2a2576e7d3fc0ee3844` from `D107fc572c438d6005491`: `N6da7f19259247dae36bf --NOT SUBREGION_OF--> Nece838c93ffafb4a6d15`.

Canonical positive-chain target: `Nece838c93ffafb4a6d15`. Denied object: `Nece838c93ffafb4a6d15`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N6da7f19259247dae36bf --SUBREGION_OF [E47f117aa50b08264f2ca; D1759848a15f03afde86d]--> Ne7800333ede839e48381 --SUBREGION_OF [E535bc9abc1e5ada65190; D7d1d491e6a497690f61d]--> Naec278f805d922d2146d --SUBREGION_OF [E123f6c8c8971a755674c; Dd4eb22dad1731a072aee]--> Nece838c93ffafb4a6d15
```

Conflict witness sets (support plus separate denial): `[["E123f6c8c8971a755674c","E47f117aa50b08264f2ca","E535bc9abc1e5ada65190","Ed2a2576e7d3fc0ee3844"]]`.

### Source documents (verbatim)

**D1759848a15f03afde86d** — shortest-path support; assertion `E47f117aa50b08264f2ca`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `5eb3b304a009d060b2e4440959bfe0700f88d914d1395154c377e544fc9983b1`.

> N6da7f19259247dae36bf is a subregion of Ne7800333ede839e48381. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D7d1d491e6a497690f61d** — shortest-path support; assertion `E535bc9abc1e5ada65190`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `4573f0b948713824c47fd551cf62b1da55f82b07b94dac2e9b3c696490b1c016`.

> Ne7800333ede839e48381 is a subregion of Naec278f805d922d2146d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd4eb22dad1731a072aee** — shortest-path support; assertion `E123f6c8c8971a755674c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `29b3271bb51e499d7760ee35f06f91cea768466ce4804852954ed2b24aa35ee0`.

> Naec278f805d922d2146d is a subregion of Nece838c93ffafb4a6d15. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D107fc572c438d6005491** — explicit denial; assertion `Ed2a2576e7d3fc0ee3844`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `0b4842b23334d59a2aefc448823cfd21df696e74a9a8d74350ee2d9beb3cdc30`.

> N6da7f19259247dae36bf is not a subregion of Nece838c93ffafb4a6d15. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4ff1724729c0dc75dac1** — unrelated distractor; assertion `E8c130267d3fd94de278c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `ff9c3e3c88fe755320596ea81ff0beacb20c95933ece2a54b4f7c4b65ce5c1a5`.

> N91eb61a5627b7001cc20 is a subregion of Ndf2fa34d9a303db22621. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D02a839711ec43f7a1d26** — unrelated distractor; assertion `Eb6120cb8e1d92d2f5c39`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `eeb21208cce0d70c607297a7739882544b16eadda8a40d7b112d35fda2494ab0`.

> N91eb61a5627b7001cc20 is a subregion of N8f750e01d50fa995fde6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 39; delivered: 39; evidence tokens: 4093.

Missing witness assertions before budget: `[["E123f6c8c8971a755674c","E535bc9abc1e5ada65190"]]`; after budget: `[["E123f6c8c8971a755674c","E535bc9abc1e5ada65190"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C8b19850343875fd938d3

Pair: **F30004** / partner **Cd232869ea3c6d7941431**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N6da7f19259247dae36bf? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ee591324c3870b202888e` from `Decaa8fc6b15beb60ce58`: `N6da7f19259247dae36bf --NOT SUBREGION_OF--> N44332c9561af96b5fbc7`.

Canonical positive-chain target: `Nece838c93ffafb4a6d15`. Denied object: `N44332c9561af96b5fbc7`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N6da7f19259247dae36bf --SUBREGION_OF [E47f117aa50b08264f2ca; D1759848a15f03afde86d]--> Ne7800333ede839e48381 --SUBREGION_OF [E535bc9abc1e5ada65190; D7d1d491e6a497690f61d]--> Naec278f805d922d2146d --SUBREGION_OF [E123f6c8c8971a755674c; Dd4eb22dad1731a072aee]--> Nece838c93ffafb4a6d15
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D1759848a15f03afde86d** — shortest-path support; assertion `E47f117aa50b08264f2ca`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `5eb3b304a009d060b2e4440959bfe0700f88d914d1395154c377e544fc9983b1`.

> N6da7f19259247dae36bf is a subregion of Ne7800333ede839e48381. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D7d1d491e6a497690f61d** — shortest-path support; assertion `E535bc9abc1e5ada65190`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `4573f0b948713824c47fd551cf62b1da55f82b07b94dac2e9b3c696490b1c016`.

> Ne7800333ede839e48381 is a subregion of Naec278f805d922d2146d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd4eb22dad1731a072aee** — shortest-path support; assertion `E123f6c8c8971a755674c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `29b3271bb51e499d7760ee35f06f91cea768466ce4804852954ed2b24aa35ee0`.

> Naec278f805d922d2146d is a subregion of Nece838c93ffafb4a6d15. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Decaa8fc6b15beb60ce58** — explicit denial; assertion `Ee591324c3870b202888e`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `3b065cd4a72c9f9e1694e4b05e3814f7cfe987f2964db7c3986908939a7ce40b`.

> N6da7f19259247dae36bf is not a subregion of N44332c9561af96b5fbc7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4ff1724729c0dc75dac1** — unrelated distractor; assertion `E8c130267d3fd94de278c`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `ff9c3e3c88fe755320596ea81ff0beacb20c95933ece2a54b4f7c4b65ce5c1a5`.

> N91eb61a5627b7001cc20 is a subregion of Ndf2fa34d9a303db22621. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D02a839711ec43f7a1d26** — unrelated distractor; assertion `Eb6120cb8e1d92d2f5c39`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `eeb21208cce0d70c607297a7739882544b16eadda8a40d7b112d35fda2494ab0`.

> N91eb61a5627b7001cc20 is a subregion of N8f750e01d50fa995fde6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4095.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C904e17d3e62812902b13

Pair: **F30005** / partner **C734bcf501f31be8fc084**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nbee61c7b321945a2c257? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E8870f14ae49d652e5b59` from `Dd1555d1f4e34553d103d`: `Nbee61c7b321945a2c257 --NOT PRECEDES--> Ne3e274fe0cf169e80492`.

Canonical positive-chain target: `Ne3e274fe0cf169e80492`. Denied object: `Ne3e274fe0cf169e80492`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
Nbee61c7b321945a2c257 --PRECEDES [E95f41d6b5f768cc3cf87; D6807e269f2e431450192]--> Nac580aee5d40acb7977c --PRECEDES [Ef3d8a29be0f6907c8360; D608a30d0fb87af0d3f49]--> N893b47622caf56edcbc1 --PRECEDES [E0864612b7ebf232487a2; D57c55226860aadafa0aa]--> Ne3e274fe0cf169e80492
```

Conflict witness sets (support plus separate denial): `[["E0864612b7ebf232487a2","E8870f14ae49d652e5b59","E95f41d6b5f768cc3cf87","Ef3d8a29be0f6907c8360"]]`.

### Source documents (verbatim)

**D6807e269f2e431450192** — shortest-path support; assertion `E95f41d6b5f768cc3cf87`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `d0d36bd9391db03bb5c12d43633b9be1f8c2c7bb9f8b8877d0902443e7d8fd57`.

> Nbee61c7b321945a2c257 precedes Nac580aee5d40acb7977c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D608a30d0fb87af0d3f49** — shortest-path support; assertion `Ef3d8a29be0f6907c8360`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `c409349fbf318018866dea79056800cfd1fc55042648ebf2a59bcbfac7ae3f21`.

> Nac580aee5d40acb7977c precedes N893b47622caf56edcbc1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D57c55226860aadafa0aa** — shortest-path support; assertion `E0864612b7ebf232487a2`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `4493735aef93f64105f388398cf859ed6d9e4c118181da4aea2dc0e751c7dfa8`.

> N893b47622caf56edcbc1 precedes Ne3e274fe0cf169e80492. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1555d1f4e34553d103d** — explicit denial; assertion `E8870f14ae49d652e5b59`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `9fbaafd89acf35441eb8758805685041dfd27839c106c15874da1aa59ade65d3`.

> Nbee61c7b321945a2c257 does not precede Ne3e274fe0cf169e80492. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D64e6b2be5897da8958a4** — unrelated distractor; assertion `E9b179d4e6f54710465a0`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `9ef9df54ec25132162ba0ce243775e3b31a23e2a117b3389b7c462759ba17bc5`.

> N7ec7642684931121b4cf precedes Nb1ba64697e47691ad304. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2b63892f95f58fe7c8b5** — unrelated distractor; assertion `E218de95ca6508569a5c1`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `53bc6079da0011d8d11cf0ac8cbeeab273af4f78f616505be75cc3c59797e722`.

> N7ec7642684931121b4cf precedes Nd9a8cd333510d81469e3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4091.

Missing witness assertions before budget: `[["E0864612b7ebf232487a2"]]`; after budget: `[["E0864612b7ebf232487a2"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C734bcf501f31be8fc084

Pair: **F30005** / partner **C904e17d3e62812902b13**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **PRECEDES**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving Nbee61c7b321945a2c257? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Edbd69ad6c4d1178681cc` from `Db4dcda9f1198705b8e51`: `Nbee61c7b321945a2c257 --NOT PRECEDES--> Nc60235a4793beff228f9`.

Canonical positive-chain target: `Ne3e274fe0cf169e80492`. Denied object: `Nc60235a4793beff228f9`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
Nbee61c7b321945a2c257 --PRECEDES [E95f41d6b5f768cc3cf87; D6807e269f2e431450192]--> Nac580aee5d40acb7977c --PRECEDES [Ef3d8a29be0f6907c8360; D608a30d0fb87af0d3f49]--> N893b47622caf56edcbc1 --PRECEDES [E0864612b7ebf232487a2; D57c55226860aadafa0aa]--> Ne3e274fe0cf169e80492
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D6807e269f2e431450192** — shortest-path support; assertion `E95f41d6b5f768cc3cf87`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `d0d36bd9391db03bb5c12d43633b9be1f8c2c7bb9f8b8877d0902443e7d8fd57`.

> Nbee61c7b321945a2c257 precedes Nac580aee5d40acb7977c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D608a30d0fb87af0d3f49** — shortest-path support; assertion `Ef3d8a29be0f6907c8360`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `c409349fbf318018866dea79056800cfd1fc55042648ebf2a59bcbfac7ae3f21`.

> Nac580aee5d40acb7977c precedes N893b47622caf56edcbc1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D57c55226860aadafa0aa** — shortest-path support; assertion `E0864612b7ebf232487a2`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `4493735aef93f64105f388398cf859ed6d9e4c118181da4aea2dc0e751c7dfa8`.

> N893b47622caf56edcbc1 precedes Ne3e274fe0cf169e80492. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db4dcda9f1198705b8e51** — explicit denial; assertion `Edbd69ad6c4d1178681cc`; sentence `s1`; span [0, 61); SHA256 of canonical JSON text `48651962de834ef9dd24a58ae991493675171f6daebe42509fbee3492438d316`.

> Nbee61c7b321945a2c257 does not precede Nc60235a4793beff228f9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D64e6b2be5897da8958a4** — unrelated distractor; assertion `E9b179d4e6f54710465a0`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `9ef9df54ec25132162ba0ce243775e3b31a23e2a117b3389b7c462759ba17bc5`.

> N7ec7642684931121b4cf precedes Nb1ba64697e47691ad304. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2b63892f95f58fe7c8b5** — unrelated distractor; assertion `E218de95ca6508569a5c1`; sentence `s1`; span [0, 53); SHA256 of canonical JSON text `53bc6079da0011d8d11cf0ac8cbeeab273af4f78f616505be75cc3c59797e722`.

> N7ec7642684931121b4cf precedes Nd9a8cd333510d81469e3. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4096.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C2d191d934a58992b6ebe

Pair: **F30006** / partner **C292080bf6559fd1f67d3**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N6a3495420695c5af6c10? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E9feaf4cfa47df1daa7ed` from `D5fdfb5f7ccc83743e7bc`: `N6a3495420695c5af6c10 --NOT CONTAINED_IN--> N88fadab90a854a2b8210`.

Canonical positive-chain target: `N88fadab90a854a2b8210`. Denied object: `N88fadab90a854a2b8210`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N6a3495420695c5af6c10 --CONTAINED_IN [E5de5ed307ea03c2b7252; D0a9a1b0bfc9101593f71]--> N89d0dbd404ec6e5dc559 --CONTAINED_IN [E45724dd9a7ae4e83665f; D70b465c9b341f3399d62]--> N8f5bae419445ccead139 --CONTAINED_IN [E330fa9dc40c41686788a; Dcdabb513ad63e698f478]--> N88fadab90a854a2b8210
```

Conflict witness sets (support plus separate denial): `[["E330fa9dc40c41686788a","E45724dd9a7ae4e83665f","E5de5ed307ea03c2b7252","E9feaf4cfa47df1daa7ed"]]`.

### Source documents (verbatim)

**D0a9a1b0bfc9101593f71** — shortest-path support; assertion `E5de5ed307ea03c2b7252`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `4f30278717602d941ef5589272d47dd9cf81874a7ecab42f33280697f2728b1f`.

> N6a3495420695c5af6c10 is contained in N89d0dbd404ec6e5dc559. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D70b465c9b341f3399d62** — shortest-path support; assertion `E45724dd9a7ae4e83665f`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `3b35fae9ad220d56cc5658deb94756e266d85219391e4af2a185f5121adbe10b`.

> N89d0dbd404ec6e5dc559 is contained in N8f5bae419445ccead139. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcdabb513ad63e698f478** — shortest-path support; assertion `E330fa9dc40c41686788a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `8fc62e300b47701236bee43061ebfdafea63912ce8b2161de2285ff61af88cfb`.

> N8f5bae419445ccead139 is contained in N88fadab90a854a2b8210. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5fdfb5f7ccc83743e7bc** — explicit denial; assertion `E9feaf4cfa47df1daa7ed`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `c1f0baba8bb70b78279bf2201785c7f640822a4e092f3be713b0a68e56b4a0d8`.

> N6a3495420695c5af6c10 is not contained in N88fadab90a854a2b8210. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5ef6a4f1888edcc4ba21** — unrelated distractor; assertion `E6119b79c239495f6fa45`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `20ee4d0900f26fbc035671b3b29f8e07b99f64121e2ea8c32d6dfa1f8d031ffe`.

> N68233fd84827a175ff68 is contained in N0c8b08d1d71a0e68da23. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Ddc7a70b23d3d5d8f9979** — unrelated distractor; assertion `E523befc3717ff42c2e53`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `693fa39af14dc86eec8773fa0e8812c8f4d7709c1efed9e441e4a29c804bca4b`.

> N68233fd84827a175ff68 is contained in N809fff7bccb145da2c73. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4087.

Missing witness assertions before budget: `[["E330fa9dc40c41686788a","E45724dd9a7ae4e83665f"]]`; after budget: `[["E330fa9dc40c41686788a","E45724dd9a7ae4e83665f"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C292080bf6559fd1f67d3

Pair: **F30006** / partner **C2d191d934a58992b6ebe**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **CONTAINED_IN**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N6a3495420695c5af6c10? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Ebf256d2a1c2b0ee6664f` from `D426cb2030d97ab194aad`: `N6a3495420695c5af6c10 --NOT CONTAINED_IN--> N5a02c2ca9cb758b9dbd1`.

Canonical positive-chain target: `N88fadab90a854a2b8210`. Denied object: `N5a02c2ca9cb758b9dbd1`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N6a3495420695c5af6c10 --CONTAINED_IN [E5de5ed307ea03c2b7252; D0a9a1b0bfc9101593f71]--> N89d0dbd404ec6e5dc559 --CONTAINED_IN [E45724dd9a7ae4e83665f; D70b465c9b341f3399d62]--> N8f5bae419445ccead139 --CONTAINED_IN [E330fa9dc40c41686788a; Dcdabb513ad63e698f478]--> N88fadab90a854a2b8210
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**D0a9a1b0bfc9101593f71** — shortest-path support; assertion `E5de5ed307ea03c2b7252`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `4f30278717602d941ef5589272d47dd9cf81874a7ecab42f33280697f2728b1f`.

> N6a3495420695c5af6c10 is contained in N89d0dbd404ec6e5dc559. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D70b465c9b341f3399d62** — shortest-path support; assertion `E45724dd9a7ae4e83665f`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `3b35fae9ad220d56cc5658deb94756e266d85219391e4af2a185f5121adbe10b`.

> N89d0dbd404ec6e5dc559 is contained in N8f5bae419445ccead139. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcdabb513ad63e698f478** — shortest-path support; assertion `E330fa9dc40c41686788a`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `8fc62e300b47701236bee43061ebfdafea63912ce8b2161de2285ff61af88cfb`.

> N8f5bae419445ccead139 is contained in N88fadab90a854a2b8210. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D426cb2030d97ab194aad** — explicit denial; assertion `Ebf256d2a1c2b0ee6664f`; sentence `s1`; span [0, 64); SHA256 of canonical JSON text `1bf37e29b055fb60ca299d477033bed3fe11e0309c04f034b8b1b8dce67794b4`.

> N6a3495420695c5af6c10 is not contained in N5a02c2ca9cb758b9dbd1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D5ef6a4f1888edcc4ba21** — unrelated distractor; assertion `E6119b79c239495f6fa45`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `20ee4d0900f26fbc035671b3b29f8e07b99f64121e2ea8c32d6dfa1f8d031ffe`.

> N68233fd84827a175ff68 is contained in N0c8b08d1d71a0e68da23. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Ddc7a70b23d3d5d8f9979** — unrelated distractor; assertion `E523befc3717ff42c2e53`; sentence `s1`; span [0, 60); SHA256 of canonical JSON text `693fa39af14dc86eec8773fa0e8812c8f4d7709c1efed9e441e4a29c804bca4b`.

> N68233fd84827a175ff68 is contained in N809fff7bccb145da2c73. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4095.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C42ca936fcf6590680a3a

Pair: **F30007** / partner **C003f7fb031839821d2d0**. Condition: **conflict**. Expected conflict: **true**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N592bdd6359cf7d78ac5e? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`Eccbb9fe323b9a426d99c` from `Dca9d139657d87fcd8fd5`: `N592bdd6359cf7d78ac5e --NOT SUBREGION_OF--> Ncd02037457c0126890b6`.

Canonical positive-chain target: `Ncd02037457c0126890b6`. Denied object: `Ncd02037457c0126890b6`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N592bdd6359cf7d78ac5e --SUBREGION_OF [Ec23f5e79bfb548f9bb61; Dd1e9c4f46e9c0f800549]--> N05b206f4e6dc4af2486b --SUBREGION_OF [E324bf33ddca21961b184; D9a3ed82160e45022573d]--> N9596269e30f654ebba35 --SUBREGION_OF [E47fd7dcfe5a75a3307e6; D117910389e4c95e887bc]--> Ncd02037457c0126890b6
```

Conflict witness sets (support plus separate denial): `[["E324bf33ddca21961b184","E47fd7dcfe5a75a3307e6","Ec23f5e79bfb548f9bb61","Eccbb9fe323b9a426d99c"]]`.

### Source documents (verbatim)

**Dd1e9c4f46e9c0f800549** — shortest-path support; assertion `Ec23f5e79bfb548f9bb61`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `5ae9e1d0f339c4923b95681fc7abfc94a46bb2fa4495dc6f237df4db0a22b0b9`.

> N592bdd6359cf7d78ac5e is a subregion of N05b206f4e6dc4af2486b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D9a3ed82160e45022573d** — shortest-path support; assertion `E324bf33ddca21961b184`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `c9d203c169b0cb57d90399a78d734bfc9541f6fb60accfc254125e11585d9406`.

> N05b206f4e6dc4af2486b is a subregion of N9596269e30f654ebba35. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D117910389e4c95e887bc** — shortest-path support; assertion `E47fd7dcfe5a75a3307e6`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1edbfc7c868f8444ceb5f8598823dde322ecb85847cab2b0a407f2fd1f58c7dd`.

> N9596269e30f654ebba35 is a subregion of Ncd02037457c0126890b6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dca9d139657d87fcd8fd5** — explicit denial; assertion `Eccbb9fe323b9a426d99c`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `6df9fd4f0df637e957d046bc87ef069e91428015e7921f16b61650f7f21368be`.

> N592bdd6359cf7d78ac5e is not a subregion of Ncd02037457c0126890b6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3836e288c402128f2f93** — unrelated distractor; assertion `Ea215db30586c81433e23`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `da9b9bf1fc169a8845be8a78202a062c730cf6c29c801eafcd5b55027aa2705f`.

> N22028d647cf22f381221 is a subregion of Nc38812fc2d03821a4ca0. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd6372989d953584ef556** — unrelated distractor; assertion `E1ddbe8cdce88764d5836`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `920c83eb2c55103dc051bde8ad9ab488908a0505a78b77453b808c2e85ec85fa`.

> N22028d647cf22f381221 is a subregion of Nd949fe095751f5117a32. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **fn**; failure: **retrieval_incomplete**. Raw source chunks: 38; delivered: 38; evidence tokens: 4095.

Missing witness assertions before budget: `[["E324bf33ddca21961b184","E47fd7dcfe5a75a3307e6"]]`; after budget: `[["E324bf33ddca21961b184","E47fd7dcfe5a75a3307e6"]]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; saved_fixture_retrieval_incomplete.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

## C003f7fb031839821d2d0

Pair: **F30007** / partner **C42ca936fcf6590680a3a**. Condition: **control**. Expected conflict: **false**. Minimum positive-chain depth: **3**. Relation: **SUBREGION_OF**.

### Question

Based only on the available source documents, is there an inconsistency in the stated relationship involving N592bdd6359cf7d78ac5e? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

### Opposing / explicit negative assertion

`E2858d82f82e168f71b12` from `D352f1dafbdc9f42eab0c`: `N592bdd6359cf7d78ac5e --NOT SUBREGION_OF--> N4a6724ddb56b4cd67179`.

Canonical positive-chain target: `Ncd02037457c0126890b6`. Denied object: `N4a6724ddb56b4cd67179`.

### All shortest positive source-backed paths

Path 1 (3 supporting hops):

```text
N592bdd6359cf7d78ac5e --SUBREGION_OF [Ec23f5e79bfb548f9bb61; Dd1e9c4f46e9c0f800549]--> N05b206f4e6dc4af2486b --SUBREGION_OF [E324bf33ddca21961b184; D9a3ed82160e45022573d]--> N9596269e30f654ebba35 --SUBREGION_OF [E47fd7dcfe5a75a3307e6; D117910389e4c95e887bc]--> Ncd02037457c0126890b6
```

Conflict witness sets (support plus separate denial): `[]`.

**Control interpretation:** the positive chain above does not end at the denied object. Independent search found no positive path to the denied object. This is absence of demonstrated contradiction, not inferred negation. There is no opposing positive proof for this denial.

### Source documents (verbatim)

**Dd1e9c4f46e9c0f800549** — shortest-path support; assertion `Ec23f5e79bfb548f9bb61`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `5ae9e1d0f339c4923b95681fc7abfc94a46bb2fa4495dc6f237df4db0a22b0b9`.

> N592bdd6359cf7d78ac5e is a subregion of N05b206f4e6dc4af2486b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D9a3ed82160e45022573d** — shortest-path support; assertion `E324bf33ddca21961b184`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `c9d203c169b0cb57d90399a78d734bfc9541f6fb60accfc254125e11585d9406`.

> N05b206f4e6dc4af2486b is a subregion of N9596269e30f654ebba35. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D117910389e4c95e887bc** — shortest-path support; assertion `E47fd7dcfe5a75a3307e6`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `1edbfc7c868f8444ceb5f8598823dde322ecb85847cab2b0a407f2fd1f58c7dd`.

> N9596269e30f654ebba35 is a subregion of Ncd02037457c0126890b6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D352f1dafbdc9f42eab0c** — explicit denial; assertion `E2858d82f82e168f71b12`; sentence `s1`; span [0, 66); SHA256 of canonical JSON text `6aa5a2ac76bcd45fa93193926a18e96fdfde8ef08c83ccec863d833943ecb0a7`.

> N592bdd6359cf7d78ac5e is not a subregion of N4a6724ddb56b4cd67179. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3836e288c402128f2f93** — unrelated distractor; assertion `Ea215db30586c81433e23`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `da9b9bf1fc169a8845be8a78202a062c730cf6c29c801eafcd5b55027aa2705f`.

> N22028d647cf22f381221 is a subregion of Nc38812fc2d03821a4ca0. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd6372989d953584ef556** — unrelated distractor; assertion `E1ddbe8cdce88764d5836`; sentence `s1`; span [0, 62); SHA256 of canonical JSON text `920c83eb2c55103dc051bde8ad9ab488908a0505a78b77453b808c2e85ec85fa`.

> N22028d647cf22f381221 is a subregion of Nd949fe095751f5117a32. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

### Saved fixture evidence and attention

Outcome: **tn**; failure: **none**. Raw source chunks: 34; delivered: 34; evidence tokens: 4089.

Missing witness assertions before budget: `[]`; after budget: `[]`.

Missing witness sentences present in raw native graph descriptions: `[]`. These do not count as exact source-chunk proof retrieval.

Review flags: human_signoff_pending; synthetic_rule_scope_and_opaque_names; model_visible_build_timestamp_condition_proxy; control_depth_labels_separate_positive_chain.

- [ ] Question/source wording matches intended fictional rule scope.
- [ ] All assertion spans, polarities, shortest paths and explicit denial are correct.
- [ ] Pair differs only in denied object; alternative condition is excluded.
- [ ] Native evidence preserves polarity; undirected graph order is not used as proof direction.
- [ ] Any retrieval miss and citation roles are reviewed without changing gold labels.
- [ ] Record reviewer, date, decision and rationale in human_review.csv.

