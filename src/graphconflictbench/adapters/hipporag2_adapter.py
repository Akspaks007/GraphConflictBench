"""Configuration and worker selection for the native HippoRAG 2 SDK."""

from typing import Literal

from pydantic import Field, model_validator

from ..schemas import Record
from .base import NativeSubprocessAdapter


class HippoRAGConfig(Record):
    architecture: Literal["hipporag2"]
    provider: Literal["fixture", "groq"]
    upstream_repository: str
    upstream_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    upstream_license: str
    llm_model: str
    embedding_model: str
    embedding_dimension: int = Field(gt=0)
    retrieval_top_k: int = Field(gt=0)
    linking_top_k: int = Field(gt=0)
    evidence_budget: int = Field(gt=0)
    max_retries: Literal[0] = 0
    benchmark_eligible: Literal[False] = False
    provider_control_file: str | None = None
    provider_control_sha256: str | None = None

    @model_validator(mode="after")
    def provider_configuration(self):
        if self.provider == "groq":
            if self.embedding_model != "BAAI/bge-small-en-v1.5" or self.embedding_dimension != 384:
                raise ValueError("Groq requires the configured 384-dimensional local BGE model")
            if not self.provider_control_file or not self.provider_control_sha256:
                raise ValueError("Groq requires a frozen capture/spending policy")
        return self


class HippoRAGAdapter(NativeSubprocessAdapter):
    config_model = HippoRAGConfig
    architecture = "hipporag2"
    name = "HippoRAG 2"
