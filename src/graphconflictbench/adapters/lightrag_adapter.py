"""Configuration and worker selection for the native LightRAG SDK."""

from typing import Literal

from pydantic import Field, model_validator

from ..schemas import Record
from .base import NativeSubprocessAdapter
from .base import implementation_hash as implementation_hash


class AdapterConfig(Record):
    architecture: Literal["lightrag"]
    provider: Literal["fixture", "openai", "gemini", "groq"]
    upstream_repository: str
    upstream_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    upstream_license: str
    python: str
    mode: Literal["hybrid", "mix", "local", "global"]
    llm_model: str
    embedding_model: str
    embedding_dimension: int = Field(gt=0)
    top_k: int = Field(gt=0)
    chunk_top_k: int = Field(gt=0)
    max_total_tokens: int = Field(gt=0)
    max_entity_tokens: int = Field(gt=0)
    max_relation_tokens: int = Field(gt=0)
    evidence_budget: int = Field(gt=0)
    chunk_token_size: int = Field(gt=0)
    chunk_overlap_token_size: int = Field(ge=0)
    max_concurrency: int = Field(gt=0)
    max_retries: int = Field(ge=0)
    extract_gleaning: int = Field(ge=0)
    cosine_threshold: float
    benchmark_eligible: bool
    provider_control_file: str | None = None
    provider_control_sha256: str | None = None
    embedding_task_type: Literal["SEMANTIC_SIMILARITY"] | None = None

    @model_validator(mode="after")
    def provider_configuration(self):
        if self.provider == "gemini":
            if self.llm_model != "gemini-2.5-flash" or self.embedding_model != "gemini-embedding-001":
                raise ValueError("Gemini model substitution requires a reviewed integration change")
            if self.embedding_dimension not in (768, 1536, 3072):
                raise ValueError("use a reviewed Gemini embedding dimension: 768, 1536 or 3072")
            if self.embedding_task_type != "SEMANTIC_SIMILARITY":
                raise ValueError("Gemini requires the same SEMANTIC_SIMILARITY task for every embedding")
            if self.max_retries != 0 or self.max_concurrency != 1:
                raise ValueError("Gemini smoke requires zero retries and concurrency one")
            if self.benchmark_eligible:
                raise ValueError("Gemini readiness smoke is not benchmark eligible")
        if self.provider == "groq":
            if self.embedding_model != "BAAI/bge-small-en-v1.5" or self.embedding_dimension != 384:
                raise ValueError("Groq requires the configured 384-dimensional local BGE model")
            if self.max_retries != 0 or self.max_concurrency != 1 or self.benchmark_eligible:
                raise ValueError("Groq smoke requires zero retries and concurrency one")
        return self


class LightRAGAdapter(NativeSubprocessAdapter):
    config_model = AdapterConfig
    architecture = "lightrag"
    name = "LightRAG"

    def _worker_timeout(self, operation):
        if self.config["provider"] != "gemini" or operation == "healthcheck":
            return 1800
        from ..gemini_control import GeminiControl

        if not self.config["provider_control_file"]:
            raise ValueError("Gemini requires a frozen quota policy before worker execution")
        policy = GeminiControl(self.config["provider_control_file"],
                               self.config["provider_control_sha256"]).policy
        # Slow quota-compliant indexing must not hit the existing 30-minute limit.
        # This is process headroom, not extra permission to dispatch: the shared
        # lifetime/day/spend/deadline guards still stop requests independently.
        calls = min(policy.max_requests, policy.max_requests_per_24h)
        return 1800 + calls * (policy.min_interval_seconds + 180)
