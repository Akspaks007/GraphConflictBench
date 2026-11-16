import json
from datetime import date
from pathlib import Path

import pytest

from graphconflictbench.reasoner import Reasoner
from graphconflictbench.schemas import Assertion, Entity

FIXTURES = json.loads((Path(__file__).parents[1] / "fixtures/logic_cases.json").read_text())


def make(ontology, predicate="CONTAINED_IN", pairs=None):
    pairs = pairs or [("A", "B"), ("B", "Z")]
    names = sorted({x for pair in pairs for x in pair} | {"A", "B", "C", "Z", "Q"})
    entities = [
        Entity(entity_id=x, name=x, type=ontology.relations[predicate].domain, family_id="F")
        for x in names
    ]
    edges = [
        Assertion(
            assertion_id=f"E{i}",
            doc_id=f"D{i}",
            sentence_id="s1",
            subject=s,
            predicate=predicate,
            object=o,
            polarity="positive",
        )
        for i, (s, o) in enumerate(pairs)
    ]
    return entities, edges


@pytest.mark.parametrize("fixture", FIXTURES, ids=[x["name"] for x in FIXTURES])
def test_twelve_hand_authored_fixtures(ontology, fixture):
    chain = fixture["chain"]
    entities, edges = make(ontology, fixture["relation"], list(zip(chain, chain[1:])))
    denial = Assertion(
        assertion_id="DENY",
        doc_id="DN",
        sentence_id="s1",
        subject="A",
        predicate=fixture["relation"],
        object=fixture["deny"],
        polarity="negative",
    )
    r = Reasoner(entities, edges + [denial], ontology)
    assert bool(r.conflicts()) is fixture["conflict"]
    assert len(r.shortest_proofs("A", fixture["relation"], "Z")[0]) == len(chain) - 1
    # Independently verify each gold edge is necessary in this fixture.
    for edge in edges:
        broken = Reasoner(entities, [a for a in edges if a != edge] + [denial], ontology)
        assert not broken.conflicts()


def test_all_alternative_minimal_proofs_and_shortcut(ontology):
    entities, edges = make(ontology, pairs=[("A", "B"), ("B", "Z"), ("A", "C"), ("C", "Z")])
    r = Reasoner(entities, edges, ontology)
    assert r.shortest_proofs("A", "CONTAINED_IN", "Z") == [("E0", "E1"), ("E2", "E3")]
    shortcut = edges[0].model_copy(update={"assertion_id": "DIRECT", "object": "Z"})
    assert Reasoner(entities, edges + [shortcut], ontology).shortest_proofs(
        "A", "CONTAINED_IN", "Z"
    ) == [("DIRECT",)]


def test_absence_and_different_subject_are_not_negation(ontology):
    entities, edges = make(ontology)
    assert not Reasoner(entities, edges, ontology).conflicts()
    denial = edges[0].model_copy(
        update={"assertion_id": "N", "subject": "Q", "object": "Z", "polarity": "negative"}
    )
    assert not Reasoner(entities, edges + [denial], ontology).conflicts()


def test_time_intersection_includes_every_edge_and_denial(ontology):
    entities, edges = make(ontology)
    edges = [
        x.model_copy(update={"valid_from": date(2026, 1, 1), "valid_to": date(2026, 2, 1)})
        for x in edges
    ]
    denial = edges[0].model_copy(
        update={
            "assertion_id": "N",
            "object": "Z",
            "polarity": "negative",
            "valid_from": date(2026, 2, 1),
            "valid_to": date(2026, 3, 1),
        }
    )
    assert not Reasoner(entities, edges + [denial], ontology).conflicts()
    denial = denial.model_copy(update={"valid_from": date(2026, 1, 15)})
    assert Reasoner(entities, edges + [denial], ontology).conflicts()
    edges[1] = edges[1].model_copy(
        update={"valid_from": date(2026, 3, 1), "valid_to": date(2026, 4, 1)}
    )
    assert not Reasoner(entities, edges + [denial], ontology).conflicts()


@pytest.mark.parametrize(
    "corruption",
    ["cycle", "unknown_predicate", "wrong_type", "duplicate", "unknown_entity", "cross_family"],
)
def test_reject_malformed_graph(ontology, corruption):
    entities, edges = make(ontology)
    if corruption == "cycle":
        edges.append(
            edges[0].model_copy(update={"assertion_id": "BACK", "subject": "Z", "object": "A"})
        )
    elif corruption == "unknown_predicate":
        edges[0] = edges[0].model_copy(update={"predicate": "WORKS_AT"})
    elif corruption == "wrong_type":
        entities[0] = entities[0].model_copy(update={"type": "event"})
    elif corruption == "duplicate":
        edges.append(edges[0])
    elif corruption == "unknown_entity":
        edges[0] = edges[0].model_copy(update={"subject": "UNKNOWN"})
    else:
        entities[0] = entities[0].model_copy(update={"family_id": "OTHER"})
    with pytest.raises(ValueError):
        Reasoner(entities, edges, ontology)


def test_nontransitive_relation_cannot_compose(ontology):
    ontology.relations["CONTAINED_IN"].transitive = False
    entities, edges = make(ontology)
    assert not Reasoner(entities, edges, ontology).shortest_proofs("A", "CONTAINED_IN", "Z")


def test_independent_closure_agrees_for_all_three_relations(ontology):
    # Boolean matrix closure is independent of shortest-path proof enumeration.
    for predicate in ontology.relations:
        entities, edges = make(ontology, predicate, [("A", "B"), ("B", "C"), ("C", "Z")])
        closure = {(a.subject, a.object) for a in edges}
        while True:
            expanded = closure | {(a, d) for a, b in closure for c, d in closure if b == c}
            if expanded == closure:
                break
            closure = expanded
        reasoner = Reasoner(entities, edges, ontology)
        for a in entities:
            for b in entities:
                assert bool(reasoner.shortest_proofs(a.entity_id, predicate, b.entity_id)) == (
                    (a.entity_id, b.entity_id) in closure
                )
