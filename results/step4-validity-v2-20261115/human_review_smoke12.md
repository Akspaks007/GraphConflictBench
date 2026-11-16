# Twelve-case human-review worksheet (v2)

Human-only gold material: never index this file or add it to model prompts. No human decision has been filled in. The existing smoke dataset is reused without alteration; all twelve cases overlap the pilot and PRECEDES is absent.

Review each question, full source text, denial, supporting direction and shortest path. For controls, depth labels the separate positive chain, not a proof to the denied object. Record accept/question/reject and a reason in the accompanying CSV. All paths and role annotations below are canonical review aids, not native graph paths.

## C3e26105ec36803f12b2e

Pair F10000; partner C96e62542ee1b2f486b9f. Condition **conflict**, expected conflict **True**, depth **1**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd3a7440e5b8f66ca8744? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"Ea51f6de09e12bc38988a","doc_id":"D8e1819f9a41f64977ff5","object":"N6401ff9770356cea0bdf","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"Nd3a7440e5b8f66ca8744","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
Nd3a7440e5b8f66ca8744 --CONTAINED_IN [E75388636843585860838; D124fdca7dba8c4b80a96]--> N6401ff9770356cea0bdf
```

Conflict witness sets (empty for controls): `[["E75388636843585860838","Ea51f6de09e12bc38988a"]]`.

Source documents (verbatim):

**D124fdca7dba8c4b80a96**

> Nd3a7440e5b8f66ca8744 is contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D8e1819f9a41f64977ff5**

> Nd3a7440e5b8f66ca8744 is not contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D567f46f31d8d3db00fc1**

> N022fd25e2d10ef843baf is contained in Nf6af6bea55f905f52c6f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6cace2e54ebc61628653**

> N022fd25e2d10ef843baf is contained in N4cd9009c6402d4c37d26. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Positive and negative claims merge on one undirected native endpoint pair; inspect both source sentences. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C96e62542ee1b2f486b9f

Pair F10000; partner C3e26105ec36803f12b2e. Condition **control**, expected conflict **False**, depth **1**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving Nd3a7440e5b8f66ca8744? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E3ebecb16ef5373787abd","doc_id":"Dfa1b226b2a08def00dc8","object":"N90b644b6fa099d0ec61b","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"Nd3a7440e5b8f66ca8744","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
Nd3a7440e5b8f66ca8744 --CONTAINED_IN [E75388636843585860838; D124fdca7dba8c4b80a96]--> N6401ff9770356cea0bdf
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**D124fdca7dba8c4b80a96**

> Nd3a7440e5b8f66ca8744 is contained in N6401ff9770356cea0bdf. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dfa1b226b2a08def00dc8**

> Nd3a7440e5b8f66ca8744 is not contained in N90b644b6fa099d0ec61b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D567f46f31d8d3db00fc1**

> N022fd25e2d10ef843baf is contained in Nf6af6bea55f905f52c6f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6cace2e54ebc61628653**

> N022fd25e2d10ef843baf is contained in N4cd9009c6402d4c37d26. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C42bbd4765e6d5519d2b2

Pair F10001; partner C221076261f1c382e4bda. Condition **conflict**, expected conflict **True**, depth **1**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N4142a55c2d046b158499? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"Edc35135bfb2f02dc716b","doc_id":"Dcf6378293bf1ac388f4e","object":"Ne66dd9afcc8a121e916d","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N4142a55c2d046b158499","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N4142a55c2d046b158499 --SUBREGION_OF [E3e90a150a45dd2fccc6d; D76413fefe6657c0277f5]--> Ne66dd9afcc8a121e916d
```

Conflict witness sets (empty for controls): `[["E3e90a150a45dd2fccc6d","Edc35135bfb2f02dc716b"]]`.

Source documents (verbatim):

**D76413fefe6657c0277f5**

> N4142a55c2d046b158499 is a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dcf6378293bf1ac388f4e**

> N4142a55c2d046b158499 is not a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db8ef2d8f24e3cb70b9e7**

> Nde4605c89d3cdd2fc4ed is a subregion of N04980f6d1f81f0aefb91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6ae5922c2a4aebab2026**

> Nde4605c89d3cdd2fc4ed is a subregion of N0d9c5caa04e6347c154b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Positive and negative claims merge on one undirected native endpoint pair; inspect both source sentences. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C221076261f1c382e4bda

Pair F10001; partner C42bbd4765e6d5519d2b2. Condition **control**, expected conflict **False**, depth **1**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N4142a55c2d046b158499? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E862736b3cc7957c1db38","doc_id":"D2c1207b84caee439eeea","object":"N2bdb8e0081aea98b6bb5","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N4142a55c2d046b158499","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N4142a55c2d046b158499 --SUBREGION_OF [E3e90a150a45dd2fccc6d; D76413fefe6657c0277f5]--> Ne66dd9afcc8a121e916d
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**D76413fefe6657c0277f5**

> N4142a55c2d046b158499 is a subregion of Ne66dd9afcc8a121e916d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2c1207b84caee439eeea**

> N4142a55c2d046b158499 is not a subregion of N2bdb8e0081aea98b6bb5. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db8ef2d8f24e3cb70b9e7**

> Nde4605c89d3cdd2fc4ed is a subregion of N04980f6d1f81f0aefb91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6ae5922c2a4aebab2026**

> Nde4605c89d3cdd2fc4ed is a subregion of N0d9c5caa04e6347c154b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C7e7d62477508e2b4388a

Pair F20000; partner C4bd4688564a242ecf137. Condition **conflict**, expected conflict **True**, depth **2**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N9e542f5f0372f5925428? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E60bdd836c6fd415b8ae7","doc_id":"D484ceaf31f69109851b6","object":"Nce7afaa048239899b51b","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N9e542f5f0372f5925428","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N9e542f5f0372f5925428 --CONTAINED_IN [E5228caa11684d9ab73cb; Dacb8c3df2f00f4b6989f]--> Neba37e9f6d5110819858
Neba37e9f6d5110819858 --CONTAINED_IN [Ee478f8ff67b9f5b66b4e; Df64f894e1735c6e17ae6]--> Nce7afaa048239899b51b
```

Conflict witness sets (empty for controls): `[["E5228caa11684d9ab73cb","E60bdd836c6fd415b8ae7","Ee478f8ff67b9f5b66b4e"]]`.

Source documents (verbatim):

**Dacb8c3df2f00f4b6989f**

> N9e542f5f0372f5925428 is contained in Neba37e9f6d5110819858. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df64f894e1735c6e17ae6**

> Neba37e9f6d5110819858 is contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D484ceaf31f69109851b6**

> N9e542f5f0372f5925428 is not contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D36fb5058c4a46729efa4**

> N0b786528fec79853affc is contained in N48d8423b237f1065adf8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2934e038681cf53c6fbd**

> N0b786528fec79853affc is contained in N6d9ef794a20ca01bae91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C4bd4688564a242ecf137

Pair F20000; partner C7e7d62477508e2b4388a. Condition **control**, expected conflict **False**, depth **2**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N9e542f5f0372f5925428? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E3943e4e4c2e3ed13b5ed","doc_id":"D39a8e0b264a8fdfff918","object":"N746149004f1f40df0cdc","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N9e542f5f0372f5925428","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N9e542f5f0372f5925428 --CONTAINED_IN [E5228caa11684d9ab73cb; Dacb8c3df2f00f4b6989f]--> Neba37e9f6d5110819858
Neba37e9f6d5110819858 --CONTAINED_IN [Ee478f8ff67b9f5b66b4e; Df64f894e1735c6e17ae6]--> Nce7afaa048239899b51b
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**Dacb8c3df2f00f4b6989f**

> N9e542f5f0372f5925428 is contained in Neba37e9f6d5110819858. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Df64f894e1735c6e17ae6**

> Neba37e9f6d5110819858 is contained in Nce7afaa048239899b51b. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D39a8e0b264a8fdfff918**

> N9e542f5f0372f5925428 is not contained in N746149004f1f40df0cdc. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D36fb5058c4a46729efa4**

> N0b786528fec79853affc is contained in N48d8423b237f1065adf8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D2934e038681cf53c6fbd**

> N0b786528fec79853affc is contained in N6d9ef794a20ca01bae91. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C7ea8d2cba383bd89ac9d

Pair F20001; partner C5ef6d9ade86682fff037. Condition **conflict**, expected conflict **True**, depth **2**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving Nc2c0024edfa5578510dc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E12865dea098d8cc7644e","doc_id":"Da175516fb4d2dd15b1c8","object":"N73aab90ad43a1c44d8b8","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"Nc2c0024edfa5578510dc","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
Nc2c0024edfa5578510dc --SUBREGION_OF [Efe8826c33f9cedcec848; D79e87d2f4d1f958bca1f]--> Nb311850e0d6f1dfede25
Nb311850e0d6f1dfede25 --SUBREGION_OF [Eb8b66fb63a602b3a9e54; De251762bf8dc191c5046]--> N73aab90ad43a1c44d8b8
```

Conflict witness sets (empty for controls): `[["E12865dea098d8cc7644e","Eb8b66fb63a602b3a9e54","Efe8826c33f9cedcec848"]]`.

Source documents (verbatim):

**D79e87d2f4d1f958bca1f**

> Nc2c0024edfa5578510dc is a subregion of Nb311850e0d6f1dfede25. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De251762bf8dc191c5046**

> Nb311850e0d6f1dfede25 is a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da175516fb4d2dd15b1c8**

> Nc2c0024edfa5578510dc is not a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D53dcc127c5efac8b5871**

> N5527bdf69bd05b287e26 is a subregion of Nb2c5d62a052f8aef12e6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da7d93ca64ddb2385286a**

> N5527bdf69bd05b287e26 is a subregion of N35e91e1cecb1ca1d2d0c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C5ef6d9ade86682fff037

Pair F20001; partner C7ea8d2cba383bd89ac9d. Condition **control**, expected conflict **False**, depth **2**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving Nc2c0024edfa5578510dc? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E48989830b3204a80c126","doc_id":"D3ef4f03e9b791e37b6ba","object":"Nc47ab82c165a565a2337","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"Nc2c0024edfa5578510dc","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
Nc2c0024edfa5578510dc --SUBREGION_OF [Efe8826c33f9cedcec848; D79e87d2f4d1f958bca1f]--> Nb311850e0d6f1dfede25
Nb311850e0d6f1dfede25 --SUBREGION_OF [Eb8b66fb63a602b3a9e54; De251762bf8dc191c5046]--> N73aab90ad43a1c44d8b8
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**D79e87d2f4d1f958bca1f**

> Nc2c0024edfa5578510dc is a subregion of Nb311850e0d6f1dfede25. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**De251762bf8dc191c5046**

> Nb311850e0d6f1dfede25 is a subregion of N73aab90ad43a1c44d8b8. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3ef4f03e9b791e37b6ba**

> Nc2c0024edfa5578510dc is not a subregion of Nc47ab82c165a565a2337. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D53dcc127c5efac8b5871**

> N5527bdf69bd05b287e26 is a subregion of Nb2c5d62a052f8aef12e6. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Da7d93ca64ddb2385286a**

> N5527bdf69bd05b287e26 is a subregion of N35e91e1cecb1ca1d2d0c. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C9ad27ae96d1771959b51

Pair F30000; partner C867476b9eda45605182a. Condition **conflict**, expected conflict **True**, depth **3**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N65700a2d6db36d25598a? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E837eb7fd6f1d87eb594b","doc_id":"D42a6ad15e475e77a44ea","object":"N5df6c26f99d2dabea078","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N65700a2d6db36d25598a","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N65700a2d6db36d25598a --CONTAINED_IN [Ecabbeafede29ec5a2b96; D3369302a126998523134]--> N4f8b6237641fd828e3d1
N4f8b6237641fd828e3d1 --CONTAINED_IN [Ea46ceeb6284181742429; D810fe8668f225c16c82c]--> N5fce270295be035aa745
N5fce270295be035aa745 --CONTAINED_IN [E60ac2b434d56c4db1105; D6d1b7dca231782eb5c7f]--> N5df6c26f99d2dabea078
```

Conflict witness sets (empty for controls): `[["E60ac2b434d56c4db1105","E837eb7fd6f1d87eb594b","Ea46ceeb6284181742429","Ecabbeafede29ec5a2b96"]]`.

Source documents (verbatim):

**D3369302a126998523134**

> N65700a2d6db36d25598a is contained in N4f8b6237641fd828e3d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D810fe8668f225c16c82c**

> N4f8b6237641fd828e3d1 is contained in N5fce270295be035aa745. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6d1b7dca231782eb5c7f**

> N5fce270295be035aa745 is contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D42a6ad15e475e77a44ea**

> N65700a2d6db36d25598a is not contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D92b87fb4dd790a9a0f2f**

> Ncbbbb26b53e20af47e6d is contained in N53ae6479da267416f91d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4028633f7f07194a89fc**

> Ncbbbb26b53e20af47e6d is contained in N608c6ed4328ab6d8bf66. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C867476b9eda45605182a

Pair F30000; partner C9ad27ae96d1771959b51. Condition **control**, expected conflict **False**, depth **3**, predicate **CONTAINED_IN**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N65700a2d6db36d25598a? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E248e1076a3c85d72abcb","doc_id":"D112f091f348d72661fce","object":"N0fa75f761a41530bd9d4","polarity":"negative","predicate":"CONTAINED_IN","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N65700a2d6db36d25598a","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N65700a2d6db36d25598a --CONTAINED_IN [Ecabbeafede29ec5a2b96; D3369302a126998523134]--> N4f8b6237641fd828e3d1
N4f8b6237641fd828e3d1 --CONTAINED_IN [Ea46ceeb6284181742429; D810fe8668f225c16c82c]--> N5fce270295be035aa745
N5fce270295be035aa745 --CONTAINED_IN [E60ac2b434d56c4db1105; D6d1b7dca231782eb5c7f]--> N5df6c26f99d2dabea078
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**D3369302a126998523134**

> N65700a2d6db36d25598a is contained in N4f8b6237641fd828e3d1. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D810fe8668f225c16c82c**

> N4f8b6237641fd828e3d1 is contained in N5fce270295be035aa745. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D6d1b7dca231782eb5c7f**

> N5fce270295be035aa745 is contained in N5df6c26f99d2dabea078. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D112f091f348d72661fce**

> N65700a2d6db36d25598a is not contained in N0fa75f761a41530bd9d4. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D92b87fb4dd790a9a0f2f**

> Ncbbbb26b53e20af47e6d is contained in N53ae6479da267416f91d. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D4028633f7f07194a89fc**

> Ncbbbb26b53e20af47e6d is contained in N608c6ed4328ab6d8bf66. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C18c3b347fd4b60f07d70

Pair F30001; partner C72bd1b5ee97f58f77f35. Condition **conflict**, expected conflict **True**, depth **3**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N8fe9e9640a4262cfd99d? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"Efe0998561ce841c0cadc","doc_id":"D0b3092068b267ade7047","object":"N6a09c8b2f74d7ae96dd7","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N8fe9e9640a4262cfd99d","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N8fe9e9640a4262cfd99d --SUBREGION_OF [E91a0ef8313a036fbf60e; Df9188b96fa8391566057]--> N6c8a83ea31d62164b287
N6c8a83ea31d62164b287 --SUBREGION_OF [E570c5a8715a0c2da81da; D84639360e642b7f63859]--> N4d25d1380a1dc3194e5f
N4d25d1380a1dc3194e5f --SUBREGION_OF [Edb8e57de3f5ac8e94f65; D3de38f34fc4fd8208986]--> N6a09c8b2f74d7ae96dd7
```

Conflict witness sets (empty for controls): `[["E570c5a8715a0c2da81da","E91a0ef8313a036fbf60e","Edb8e57de3f5ac8e94f65","Efe0998561ce841c0cadc"]]`.

Source documents (verbatim):

**Df9188b96fa8391566057**

> N8fe9e9640a4262cfd99d is a subregion of N6c8a83ea31d62164b287. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D84639360e642b7f63859**

> N6c8a83ea31d62164b287 is a subregion of N4d25d1380a1dc3194e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3de38f34fc4fd8208986**

> N4d25d1380a1dc3194e5f is a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D0b3092068b267ade7047**

> N8fe9e9640a4262cfd99d is not a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3bf755801edbd55b30c7**

> Nf2b79bb0ae62811bda41 is a subregion of N1ccedfeba71398b7cdb9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1b71a1b0a096adfd662**

> Nf2b79bb0ae62811bda41 is a subregion of Nb41ba5e6f39521b6e691. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.

## C72bd1b5ee97f58f77f35

Pair F30001; partner C18c3b347fd4b60f07d70. Condition **control**, expected conflict **False**, depth **3**, predicate **SUBREGION_OF**.

Question: Based only on the available source documents, is there an inconsistency in the stated relationship involving N8fe9e9640a4262cfd99d? If yes, identify each incompatible claim and cite the exact source statements needed to establish it. If not, say no conflict. Do not assume a missing claim is false.

Opposing assertion: `{"assertion_id":"E138b172bc81a8b1ab899","doc_id":"Db050aa36b577efe8b565","object":"Ne0c5ea0e185fd8d3c041","polarity":"negative","predicate":"SUBREGION_OF","schema_version":"1.0","sentence_id":"s1","source_kind":"synthetic_document","subject":"N8fe9e9640a4262cfd99d","valid_from":null,"valid_to":null}`.

All shortest positive proof paths:

```text
N8fe9e9640a4262cfd99d --SUBREGION_OF [E91a0ef8313a036fbf60e; Df9188b96fa8391566057]--> N6c8a83ea31d62164b287
N6c8a83ea31d62164b287 --SUBREGION_OF [E570c5a8715a0c2da81da; D84639360e642b7f63859]--> N4d25d1380a1dc3194e5f
N4d25d1380a1dc3194e5f --SUBREGION_OF [Edb8e57de3f5ac8e94f65; D3de38f34fc4fd8208986]--> N6a09c8b2f74d7ae96dd7
```

Conflict witness sets (empty for controls): `[]`.

Source documents (verbatim):

**Df9188b96fa8391566057**

> N8fe9e9640a4262cfd99d is a subregion of N6c8a83ea31d62164b287. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D84639360e642b7f63859**

> N6c8a83ea31d62164b287 is a subregion of N4d25d1380a1dc3194e5f. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3de38f34fc4fd8208986**

> N4d25d1380a1dc3194e5f is a subregion of N6a09c8b2f74d7ae96dd7. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Db050aa36b577efe8b565**

> N8fe9e9640a4262cfd99d is not a subregion of Ne0c5ea0e185fd8d3c041. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**D3bf755801edbd55b30c7**

> Nf2b79bb0ae62811bda41 is a subregion of N1ccedfeba71398b7cdb9. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

**Dd1b71a1b0a096adfd662**

> Nf2b79bb0ae62811bda41 is a subregion of Nb41ba5e6f39521b6e691. This registry entry describes the stated relationship in the current fictional reference world. The entry records a source assertion without evaluating other registry entries.

Possible ambiguities / review attention: Human signoff pending; fictional ontology only; opaque names. Denied object differs from positive-chain target; no contradictory positive proof is licensed by missing claims. Historical timestamp proxy is excluded by v2 allowlist; live extraction fidelity remains unmeasured.

- [ ] Source text, polarity and source spans are faithful.
- [ ] Shortest proof and denial roles are correct; control semantics are clear.
- [ ] Pair/isolation and live extraction fidelity reviewed.
- [ ] Reviewer, date, decision and rationale entered in CSV.
