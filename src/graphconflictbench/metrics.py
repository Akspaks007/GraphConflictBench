"""Small smoke-slice scorer. Official statistical evaluation is out of scope."""

from .evidence_mapper import align_citations, align_role_citations


def prf(predicted, expected):
    predicted, expected = set(predicted), set(expected)
    tp = len(predicted & expected)
    precision = tp / len(predicted) if predicted else 0.0
    recall = tp / len(expected) if expected else 0.0
    f1 = 2 * tp / (len(predicted) + len(expected)) if predicted or expected else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def score_case(case, retrieval, prediction, documents, assertions):
    roles = score_roles(case, retrieval, prediction, documents, assertions)
    if prediction is None:
        return {
            "case_id": case.case_id,
            "outcome": "error",
            "localization_f1": 0.0,
            "exact_proof_set": False,
            "complete_proof_retrieved": False,
            "failure": "generation_error",
            **roles,
        }
    mapped, errors = align_citations(prediction, retrieval, documents, assertions)
    delivered = {a for i in retrieval.retrieved_items for a in i.mapped_assertion_ids}
    complete = any(set(p) <= delivered for p in case.gold_proof_sets) if case.gold_label else None
    outcome = (
        ("tp" if prediction.conflict_detected else "fn")
        if case.gold_label
        else ("fp" if prediction.conflict_detected else "tn")
    )
    loc = max((prf(mapped, p)["f1"] for p in case.gold_proof_sets), default=0.0)
    exact = any(set(mapped) == set(p) for p in case.gold_proof_sets) and not errors
    if outcome != "tp":
        loc, exact = 0.0, False
    failure = (
        "false_positive"
        if outcome == "fp"
        else "retrieval_incomplete"
        if case.gold_label and not complete
        else "post_retrieval_detection_miss"
        if outcome == "fn"
        else "localization_miss"
        if outcome == "tp" and not exact
        else None
    )
    return {
        "case_id": case.case_id,
        "outcome": outcome,
        "complete_proof_retrieved": complete,
        "localization_f1": loc,
        "exact_proof_set": exact,
        "mapped_citations": mapped,
        "citation_errors": errors,
        "failure": failure,
        "edge_mapping_scope": "verbatim_source_chunks_only",
        **roles,
    }


def score_roles(case, retrieval, prediction, documents, assertions):
    """v2: role-tagged F1 and per-conflict exact witnesses, not an untyped union.

    Controls/errors/non-detections score zero. Each reported conflict must match
    one complete shortest witness; evidence split across conflicts cannot pass.
    This still does not evaluate explanation quality or establish source truth.
    """
    result = {
        "role_metric_version": "2.0",
        "support_localization_f1": 0.0,
        "opposing_localization_f1": 0.0,
        "role_aware_localization_f1": 0.0,
        "role_aware_exact_proof_set": False,
        "role_citation_errors": [],
    }
    if prediction is None or not case.gold_label or not prediction.conflict_detected:
        return result
    gold = [
        (set(support), {pair["negative_edge_id"]})
        for pair in case.gold_conflict_pairs
        for support in pair["minimal_support_edge_sets"]
    ]
    exact_rows, predicted_support, predicted_opposing = [], set(), set()
    for conflict in prediction.conflicts:
        support, se = align_role_citations(conflict.support, retrieval, documents, assertions)
        opposing, oe = align_role_citations(conflict.opposing, retrieval, documents, assertions)
        predicted_support.update(support)
        predicted_opposing.update(opposing)
        result["role_citation_errors"].extend(se + oe)
        exact_rows.append(any(support == s and opposing == o for s, o in gold) and not se + oe)
    tagged = {("support", a) for a in predicted_support} | {
        ("opposing", a) for a in predicted_opposing
    }
    result.update(
        support_localization_f1=max((prf(predicted_support, s)["f1"] for s, _ in gold), default=0),
        opposing_localization_f1=max((prf(predicted_opposing, o)["f1"] for _, o in gold), default=0),
        role_aware_localization_f1=max(
            (prf(tagged, {("support", a) for a in s} | {("opposing", a) for a in o})["f1"]
             for s, o in gold), default=0
        ),
        role_aware_exact_proof_set=bool(exact_rows) and all(exact_rows),
    )
    return result


def aggregate(rows):
    counts = {k: sum(r["outcome"] == k for r in rows) for k in ("tp", "tn", "fp", "fn", "error")}
    tp, fp, fn = (counts[k] for k in ("tp", "fp", "fn"))
    # Error rows remain in total and valid-output rate; metric-specific denominators explicit.
    return {
        "cases": len(rows),
        **counts,
        "valid_output_rate": (len(rows) - counts["error"]) / len(rows) if rows else None,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall_valid_rows": tp / (tp + fn) if tp + fn else None,
        "f1_valid_rows": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
    }
