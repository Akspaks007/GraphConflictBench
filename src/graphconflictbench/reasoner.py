"""Bounded-world proof enumerator. Open world; explicit negation only.

All simple positive directed paths are enumerated. Only declared transitivity
licenses compositions. Time intervals are intersected across every proof edge
and the denial, so disjoint timestamps never produce a conflict.
"""

from collections import defaultdict
from datetime import date

import yaml
from pydantic import Field, model_validator

from .manifests import digest
from .schemas import Record


class Relation(Record):
    domain: str
    range: str
    transitive: bool
    irreflexive: bool
    allow_negation: bool


class Ontology(Record):
    relations: dict[str, Relation] = Field(min_length=1)

    @model_validator(mode="after")
    def composition_types(self):
        for rule in self.relations.values():
            if rule.transitive and rule.domain != rule.range:
                raise ValueError("transitive relation must have composable domain/range")
        return self

    @classmethod
    def load(cls, path):
        return cls.model_validate(yaml.safe_load(open(path, encoding="utf-8")))


def overlap(edges, window=(None, None)):
    starts = [x.valid_from for x in edges if x.valid_from] + ([window[0]] if window[0] else [])
    ends = [x.valid_to for x in edges if x.valid_to] + ([window[1]] if window[1] else [])
    return max(starts, default=date.min) < min(ends, default=date.max)


class Reasoner:
    def __init__(self, entities, assertions, ontology):
        self.ontology = ontology
        self.entities = {x.entity_id: x for x in entities}
        self.assertions = {x.assertion_id: x for x in assertions}
        if len(self.entities) != len(entities) or len(self.assertions) != len(assertions):
            raise ValueError("duplicate entity/assertion ID")
        self.positive = defaultdict(list)
        self.negative = []
        for a in assertions:
            rule = ontology.relations.get(a.predicate)
            if rule is None:
                raise ValueError(f"undefined predicate: {a.predicate}")
            if a.subject not in self.entities or a.object not in self.entities:
                raise ValueError("assertion references unknown entity")
            if (
                self.entities[a.subject].type != rule.domain
                or self.entities[a.object].type != rule.range
            ):
                raise ValueError("relation type mismatch")
            if self.entities[a.subject].family_id != self.entities[a.object].family_id:
                raise ValueError("cross-family edge")
            if a.polarity == "positive":
                self.positive[(a.predicate, a.subject)].append(a)
            elif rule.allow_negation:
                self.negative.append(a)
            else:
                raise ValueError("explicit negation forbidden by ontology")
        self._check_cycles()

    def _check_cycles(self):
        for predicate, rule in self.ontology.relations.items():
            if not rule.irreflexive:
                continue
            visited, stack = set(), set()

            def visit(node):
                if node in stack:
                    raise ValueError(f"cycle in {predicate}")
                if node in visited:
                    return
                stack.add(node)
                for edge in self.positive[(predicate, node)]:
                    visit(edge.object)
                stack.remove(node)
                visited.add(node)

            for node in self.entities:
                visit(node)

    def shortest_proofs(self, subject, predicate, obj, window=(None, None)):
        rule = self.ontology.relations[predicate]
        solutions = []

        def walk(node, path, seen):
            if solutions and len(path) >= min(map(len, solutions)):
                return
            for edge in self.positive[(predicate, node)]:
                if edge.object in seen:
                    continue
                extended = path + [edge]
                if not overlap(extended, window):
                    continue
                if edge.object == obj:
                    solutions.append(extended)
                elif rule.transitive:
                    walk(edge.object, extended, seen | {edge.object})

        walk(subject, [], {subject})
        if not solutions:
            return []
        minimum = min(map(len, solutions))
        return sorted(
            {tuple(e.assertion_id for e in proof) for proof in solutions if len(proof) == minimum}
        )

    def conflicts(self):
        found = []
        for denial in self.negative:
            proofs = self.shortest_proofs(
                denial.subject,
                denial.predicate,
                denial.object,
                (denial.valid_from, denial.valid_to),
            )
            if proofs:
                found.append(
                    {
                        "negative_edge_id": denial.assertion_id,
                        "minimal_support_edge_sets": [list(x) for x in proofs],
                    }
                )
        return found

    def certificate(self, case):
        proofs = self.shortest_proofs(case.subject, case.relation_family, case.target_object)
        conflicts = self.conflicts()
        if not proofs or len(proofs[0]) != case.hop_depth:
            raise ValueError(f"incorrect minimum inference depth: {case.case_id}")
        expected = []
        for match in conflicts:
            for support in match["minimal_support_edge_sets"]:
                expected.append(sorted([*support, match["negative_edge_id"]]))
        if bool(conflicts) != case.gold_label:
            raise ValueError(f"incorrect conflict label: {case.case_id}")
        if case.gold_label and (
            len(conflicts) != 1 or conflicts[0]["negative_edge_id"] != case.negative_edge_id
        ):
            raise ValueError("unintended conflict")
        if sorted(expected) != sorted([sorted(x) for x in case.gold_proof_sets]):
            raise ValueError("gold witness does not match all shortest proofs")
        if conflicts != case.gold_conflict_pairs:
            raise ValueError("gold conflict pairs mismatch")
        result = {
            "schema_version": "1.0",
            "family_id": case.family_id,
            "condition": case.condition,
            "minimum_depth": len(proofs[0]),
            "positive_conclusion": [case.subject, case.relation_family, case.target_object],
            "minimal_support_edge_sets": [list(x) for x in proofs],
            "negative_edge_id": case.negative_edge_id,
            "conflicts": conflicts,
            "ontology_hash": digest(self.ontology.model_dump(mode="json")),
            "graph_hash": digest(
                [
                    a.model_dump(mode="json")
                    for a in sorted(self.assertions.values(), key=lambda a: a.assertion_id)
                ]
            ),
        }
        return {**result, "certificate_hash": digest(result)}
