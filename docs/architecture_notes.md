# LightRAG integration

Official repository: https://github.com/HKUDS/LightRAG

Pinned commit: f615931d6ab60b179d5347f92a29f75dcff776a6

Observed package: lightrag-hku 1.5.8, Python >=3.11, MIT.

The worker uses LightRAG.initialize_storages(), ainsert(texts, ids, file_paths),
aquery_data(query, QueryParam(mode="hybrid", only_need_context=True, ...)), and
finalize_storages(). Native strict document-status reads ensure all expected
documents were processed; a successful process exit alone is insufficient.
Upstream extraction stores undirected relationships, so canonical directed proof
paths are never inferred from native endpoint order.

Stored data include native entities/relationships/chunks/references, metadata,
keyword output, source paths/chunk IDs, logs, actual response and model usage
when exposed. Query snapshots are temporary copies of immutable built indexes,
because keyword retrieval may mutate native caches. Query wall time includes
subprocess startup and snapshot copying and is labelled retrieval_ms; it is not
a clean upstream algorithm-only latency measurement.

The adapter does not expose native relation-path IDs or claim-survival audits.
Those fields remain unobservable. Exact edge mappings refer to canonical source
assertions justified by delivered text, not an invented native graph alignment.

This document records the original LightRAG integration. The
[HippoRAG 2 integration](hipporag2.md) has its own native CLI profile and worker.

