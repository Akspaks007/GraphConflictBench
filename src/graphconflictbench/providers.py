"""Provider selection only; the existing OpenAI wrapper is unchanged."""

from .models import OpenAIModels


def model_provider(config):
    provider = config["provider"]
    if provider == "fixture":
        return None
    if provider == "openai":
        return OpenAIModels(config)
    if provider == "gemini":
        from .gemini_models import GeminiModels
        return GeminiModels(config)
    raise ValueError("unsupported model provider")
