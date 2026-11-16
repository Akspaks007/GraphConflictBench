"""Shared generation seam for the LightRAG smoke slice, with raw JSON retained."""

import asyncio
import json

from .models import parse_statements
from .providers import model_provider
from .schemas import Citation, Conflict, Prediction


def fixture_prediction(case, retrieval):
    # Independent text-only test generator. No canonical graph/label/proof access.
    edges, denials = [], []
    for item in retrieval.retrieved_items:
        if not item.doc_id:
            continue
        for subject, predicate, positive, obj, quote in parse_statements(item.text):
            row = (subject, predicate, obj, Citation(doc_id=item.doc_id, quote=quote))
            (edges if positive else denials).append(row)
    for subject, predicate, obj, denial in denials:
        if subject not in case.query:
            continue
        queue = [(subject, [], {subject})]
        while queue:
            node, proof, seen = queue.pop(0)
            for s, p, target, citation in edges:
                if s != node or p != predicate or target in seen:
                    continue
                if target == obj:
                    return Prediction(
                        case_id=case.case_id,
                        conflict_detected=True,
                        evidence_status="complete",
                        conflicts=[
                            Conflict(
                                support=proof + [citation],
                                opposing=[denial],
                                brief_explanation="Delivered source statements entail "
                                "a relationship explicitly denied by another source.",
                            )
                        ],
                    )
                queue.append((target, proof + [citation], seen | {target}))
    return Prediction(
        case_id=case.case_id, conflict_detected=False, evidence_status="insufficient", conflicts=[]
    )


def generate_prediction(config, system, prompt, case, retrieval):
    if config["provider"] == "fixture":
        raw = fixture_prediction(case, retrieval).model_dump_json()
        usage = []
    else:
        models = model_provider(config)
        async def invoke():
            try:
                return await models.llm(prompt, system_prompt=system)
            finally:
                await models.client.close()
        raw = asyncio.run(invoke())
        usage = models.usage
    # Strict parse; no JSON repair, no retries that silently select a successful answer.
    try:
        prediction = Prediction.model_validate_json(raw)
        if prediction.case_id != case.case_id:
            raise ValueError("prediction case_id differs from requested case")
        return raw, prediction, None, usage
    except ValueError as error:
        return raw, None, str(error), usage


def serialize_prediction(raw, prediction, error, usage):
    return {
        "raw": raw,
        "prediction": prediction.model_dump() if prediction else None,
        "parse_error": error,
        "usage": json.loads(json.dumps(usage)),
    }
