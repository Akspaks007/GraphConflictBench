"""Configuration and snapshot handling for Microsoft GraphRAG Local Search."""

import sys
from typing import Literal

from pydantic import Field, model_validator

from ..schemas import Record
from .base import NativeSubprocessAdapter


class MicrosoftGraphRAGConfig(Record):
    architecture: Literal["microsoft_graphrag"]
    provider: Literal["fixture", "groq"]
    upstream_version: Literal["3.1.0"]
    upstream_commit: Literal["7fc6607edda3d387d23e52ededbf8a75b6730f97"]
    llm_model: str
    embedding_model: str
    embedding_dimension: int = Field(gt=0)
    top_k_entities: int = Field(gt=0)
    top_k_relationships: int = Field(gt=0)
    community_level: int = Field(ge=0)
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


class MicrosoftGraphRAGAdapter(NativeSubprocessAdapter):
    config_model = MicrosoftGraphRAGConfig
    architecture = "microsoft_graphrag"
    name = "Microsoft GraphRAG Local Search"

    def index(self, corpus_manifest, index_dir, resume=False, batch_size=None):
        if batch_size is not None:
            raise ValueError("Microsoft GraphRAG builds communities over the complete corpus")
        return super().index(corpus_manifest, index_dir, resume, batch_size=sys.maxsize)

    def _worker_timeout(self, operation):
        return 21600 if operation == "index" else super()._worker_timeout(operation)

    def _index_worker_options(self, index_dir):
        return {"completion_cache": str(index_dir / "model-cache")}
