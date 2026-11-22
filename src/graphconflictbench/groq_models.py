"""Groq chat completions paired with local BGE embeddings."""

from functools import cached_property
from pathlib import Path

from .environment import groq_key_pool
from .models import OpenAIModels


class GroqModels(OpenAIModels):
    key_name = "GROQ_API_KEY"
    base_url = "https://api.groq.com/openai/v1"

    def api_keys(self):
        return groq_key_pool() or super().api_keys()

    @cached_property
    def local_embedding(self):
        from fastembed import TextEmbedding

        cache = Path(__file__).resolve().parents[2] / ".venv-lightrag" / "fastembed-cache"
        return TextEmbedding(
            model_name=self.config["embedding_model"],
            cache_dir=str(cache),
            local_files_only=True,
            threads=1,
        )

    def completion_options(self):
        return {
            "max_completion_tokens": self.control.policy.max_completion_tokens,
            "reasoning_effort": "low",
        }

    async def embedding(self, texts, **kwargs):
        import numpy as np

        shape = (len(texts), self.config["embedding_dimension"])
        if not texts:
            return np.empty(shape, dtype=np.float32)
        vectors = np.asarray(list(self.local_embedding.embed(texts)), dtype=np.float32)
        if vectors.shape != shape or not np.isfinite(vectors).all():
            raise ValueError("invalid local embedding vectors")
        return vectors
