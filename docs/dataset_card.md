# Dataset card: synthetic pilot v1.0

- 24 fictional families, 48 paired cases: 8 conflict and 8 control at each depth.
- Three relation families, distributed 3/3/2 across the eight families per depth.
- 144 unique source documents: shared support/distractors plus two denial variants.
- Each condition corpus contains 120 documents; variants are never indexed together.
- 192 entities, 144 asserted edges and 48 proof certificates.
- Seed 42; deterministic source templates, opaque names and stable neutral IDs.
- Pilot only; no train/test performance claims or statistical power guarantee.

The documents are synthetic assertions, not real-world facts or a preferred
source of truth. A contradiction does not designate either claim as true.
Canonical assertions and derivations are separate objects.

Files: entities.jsonl, documents.jsonl, assertions.jsonl, cases.jsonl, proofs.jsonl,
dataset_manifest.json, human_audit.csv and corpora/{split}/{condition}/ exports.
Document checksums use SHA256 over the canonical JSON string of the text; file
checksums use raw file bytes. Dataset hashes bind identity and file checksums.

Automatic audit checks labels, minimum depth, text-to-assertion coverage, unique
IDs, source spans, graph types/cycles, paired questions, split isolation and exact
condition-specific corpus exports. Each gold shortest proof plus denial is
recorded; controls have empty conflict witness sets and a supporting-chain
certificate.

Human textual review is pending. Copy human_audit.csv to a separate review file
before annotating it, so the generated snapshot's checksums remain valid.
The source language and templates are deliberately narrow; real-world external
validity, paraphrase robustness and trained lexical-leakage baselines remain
unmeasured. Neutral IDs and identical paired questions reduce simple leakage but
do not prove its absence.

