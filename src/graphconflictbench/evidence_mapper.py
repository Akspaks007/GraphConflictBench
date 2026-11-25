"""Conservative exact-text mapping. Never replace retrieved chunks with gold docs."""

import re

from .schemas import RetrievedItem


def map_chunk(chunk, documents, assertions, rank):
    path = chunk.get("file_path", "")
    # A chunk must identify exactly one neutral source; aggregated paths are ambiguous.
    match = re.fullmatch(r"(D[0-9a-f]{20})\.txt", path)
    doc_id = match.group(1) if match else None
    docs = {d.doc_id: d for d in documents}
    text = chunk.get("content", "")
    mapped = []
    if doc_id in docs and text and text in docs[doc_id].text:
        d = docs[doc_id]
        for a in assertions:
            if a.doc_id != doc_id:
                continue
            span = next((s for s in d.sentence_spans if s.sentence_id == a.sentence_id), None)
            if span and d.text[span.start : span.end] in text:
                mapped.append(a.assertion_id)
    return RetrievedItem(
        rank=rank,
        doc_id=doc_id if doc_id in docs else None,
        text=text,
        native_score=chunk.get("native_score"),
        native_chunk_id=chunk.get("chunk_id"),
        mapped_assertion_ids=mapped,
        mapping_status="exact_quote" if mapped else "unmapped",
    )


def align_citations(prediction, retrieval, documents, assertions):
    available = {i.doc_id: i.text for i in retrieval.retrieved_items if i.doc_id}
    docs = {d.doc_id: d for d in documents}
    matched, errors = set(), []
    for conflict in prediction.conflicts:
        for citation in conflict.support + conflict.opposing:
            source = available.get(citation.doc_id, "")
            if citation.quote not in source or citation.doc_id not in docs:
                errors.append(
                    {"doc_id": citation.doc_id, "error": "quote_not_in_delivered_evidence"}
                )
                continue
            doc = docs[citation.doc_id]
            for a in assertions:
                if a.doc_id != doc.doc_id:
                    continue
                span = next(s for s in doc.sentence_spans if s.sentence_id == a.sentence_id)
                if doc.text[span.start : span.end] in citation.quote:
                    matched.add(a.assertion_id)
    return sorted(matched), errors


def align_role_citations(citations, retrieval, documents, assertions):
    """Strict citation mapping for v2 metrics; keep legacy alignment unchanged."""
    docs = {d.doc_id: d for d in documents}
    matched, errors = set(), []
    for citation in citations:
        chunks = [i.text for i in retrieval.retrieved_items if i.doc_id == citation.doc_id]
        doc = docs.get(citation.doc_id)
        ids = set()
        # Require the quote in one delivered chunk AND the original document.
        if doc and citation.quote in doc.text and any(citation.quote in c for c in chunks):
            for a in assertions:
                if a.doc_id == doc.doc_id:
                    span = next(s for s in doc.sentence_spans if s.sentence_id == a.sentence_id)
                    if doc.text[span.start : span.end] in citation.quote:
                        ids.add(a.assertion_id)
        if not ids:
            errors.append({"doc_id": citation.doc_id, "error": "no_source_assertion_in_quote"})
        matched.update(ids)
    return matched, errors
