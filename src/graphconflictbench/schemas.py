"""Strict source, graph, evidence and prediction contracts (schema 1.0)."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    schema_version: Literal["1.0"] = "1.0"


class Entity(Record):
    entity_id: str
    name: str
    type: str
    family_id: str


class Span(Record):
    sentence_id: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)

    @model_validator(mode="after")
    def order(self):
        if self.end <= self.start:
            raise ValueError("empty/reversed sentence span")
        return self


class Document(Record):
    doc_id: str
    family_id: str
    condition: Literal["shared", "conflict", "control"]
    split: Literal["pilot", "design", "dev", "test"]
    text: str = Field(min_length=1)
    sentence_spans: list[Span]
    source_metadata: dict = Field(default_factory=lambda: {"kind": "synthetic_document"})
    checksum: str


class Assertion(Record):
    assertion_id: str
    doc_id: str
    sentence_id: str
    subject: str
    predicate: str
    object: str
    polarity: Literal["positive", "negative"]
    valid_from: date | None = None
    valid_to: date | None = None
    source_kind: Literal["synthetic_document"] = "synthetic_document"

    @model_validator(mode="after")
    def interval(self):
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValueError("validity intervals are half-open and must be nonempty")
        return self


class Case(Record):
    case_id: str
    family_id: str
    split: Literal["pilot", "design", "dev", "test"]
    condition: Literal["conflict", "control"]
    hop_depth: int = Field(ge=1, le=3)
    relation_family: str
    query: str
    subject: str
    target_object: str
    negative_edge_id: str
    gold_label: bool
    gold_proof_sets: list[list[str]]
    gold_conflict_pairs: list[dict]


class RetrievedItem(Record):
    rank: int = Field(ge=1)
    doc_id: str | None
    text: str
    native_score: float | None = None
    native_chunk_id: str | None = None
    mapped_assertion_ids: list[str] = Field(default_factory=list)
    mapping_status: Literal["exact_quote", "unmapped"] = "unmapped"


class Retrieval(Record):
    run_id: str
    architecture: Literal["lightrag", "hipporag2", "pathrag", "microsoft_graphrag"] = "lightrag"
    case_id: str
    retrieval_ms: float
    context_tokens: int
    retrieved_items: list[RetrievedItem]
    capture_complete: bool
    native_status: str
    adapter_warnings: list[str]
    native_answer: None = None
    retrieved_graph_path_length: None = None
    benchmark_eligible: bool
    native_graph: dict = Field(default_factory=dict)


class Citation(Record):
    doc_id: str
    quote: str = Field(min_length=1)


class Conflict(Record):
    support: list[Citation] = Field(min_length=1)
    opposing: list[Citation] = Field(min_length=1)
    brief_explanation: str


class Prediction(Record):
    case_id: str
    conflict_detected: bool
    evidence_status: Literal["complete", "insufficient"]
    conflicts: list[Conflict]
    resolution: Literal["not_attempted"] = "not_attempted"

    @model_validator(mode="after")
    def consistent(self):
        if self.conflict_detected != bool(self.conflicts):
            raise ValueError("conflict_detected must agree with conflicts")
        if self.conflict_detected and self.evidence_status != "complete":
            raise ValueError("a demonstrated conflict requires complete evidence")
        return self
