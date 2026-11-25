"""Configuration for the pinned native PathRAG worker."""

from typing import Literal

from pydantic import Field, model_validator

from ..schemas import Record
from .base import NativeSubprocessAdapter


class PathRAGConfig(Record):
    architecture: Literal["pathrag"]
    provider: Literal["fixture", "groq"]
    upstream_repository: str
    upstream_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    llm_model: str
    embedding_model: str
    embedding_dimension: int = Field(gt=0)
    retrieval_top_k: int = Field(gt=0)
    cosine_threshold: float = Field(ge=-1, le=1)
    evidence_budget: Literal[3072] = 3072
    benchmark_eligible: Literal[False] = False
    provider_control_file: str | None = None
    provider_control_sha256: str | None = None

    @model_validator(mode="after")
    def provider_configuration(self):
        if self.provider == "groq":
            if (self.llm_model, self.embedding_model, self.embedding_dimension) != (
                "openai/gpt-oss-20b", "BAAI/bge-small-en-v1.5", 384,
            ):
                raise ValueError("Groq requires GPT-OSS 20B and 384-dimensional local BGE")
            if not self.provider_control_file or not self.provider_control_sha256:
                raise ValueError("Groq requires a frozen capture/spending policy")
        return self


class PathRAGAdapter(NativeSubprocessAdapter):
    config_model = PathRAGConfig
    architecture = "pathrag"
    name = "PathRAG"
