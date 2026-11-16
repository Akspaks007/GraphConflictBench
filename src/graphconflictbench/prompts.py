import re
from pathlib import Path

from .manifests import canonical, digest
from .schemas import Prediction

# Versioned presentation contract; raw native responses stay in audit traces.
GRAPH_FIELDS = {
    "entities": ("entity_name", "entity_type", "description", "file_path"),
    "relationships": ("src_id", "tgt_id", "keywords", "description", "file_path"),
    "references": ("reference_id", "file_path"),
}


def model_visible_graph(graph):
    """Drop unknown keys and nested values, including build/gold metadata.

    Strings in descriptions remain untrusted native content, not verified claims.
    No canonical graph, assertion mapping or gold label is consulted here.
    """
    def allowed(key, value):
        if not isinstance(value, str):
            return False
        if key == "file_path":
            return bool(value) and all(
                re.fullmatch(r"D[0-9a-f]{20}\.txt", p) for p in value.split("<SEP>")
            )
        if key == "reference_id":
            return bool(re.fullmatch(r"[0-9]+", value))
        return True

    return {
        name: [
            {key: row[key] for key in keys if allowed(key, row.get(key))}
            for row in graph.get(name, [])
            if isinstance(row, dict)
        ]
        for name, keys in GRAPH_FIELDS.items()
    }


def evidence_envelope(retrieval):
    return {
        "sources": [
            {"doc_id": i.doc_id, "text": i.text, "rank": i.rank} for i in retrieval.retrieved_items
        ],
        "native_graph": model_visible_graph(retrieval.native_graph),
    }


def build_prompt(case, retrieval, ontology, prompt_file):
    system = Path(prompt_file).read_text(encoding="utf-8")
    rules = [
        {
            "predicate": name,
            "transitive": rule.transitive,
            "irreflexive": rule.irreflexive,
            "explicit_negation": rule.allow_negation,
        }
        for name, rule in ontology.relations.items()
    ]
    payload = {
        "case_id": case.case_id,
        "question": case.query,
        "rules": rules,
        "evidence": evidence_envelope(retrieval),
        "response_schema": Prediction.model_json_schema(),
    }
    return system, canonical(payload), digest({"system": system, "payload": payload})
