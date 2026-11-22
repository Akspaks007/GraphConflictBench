"""Select the configured generation and embedding callbacks."""

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
    if provider == "groq":
        from .groq_models import GroqModels
        return GroqModels(config)
    raise ValueError("unsupported model provider")
