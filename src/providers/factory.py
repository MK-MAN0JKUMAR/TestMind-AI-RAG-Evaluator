from src.providers.groq_provider import GroqProvider
from src.providers.ollama_provider import OllamaProvider


class LLMFactory:

    _providers = {
        "ollama": OllamaProvider,
        "groq": GroqProvider,
    }

    @classmethod
    def create(cls, provider_name, config, purpose):

        provider_name = provider_name.lower()

        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported provider: {provider_name}")

        provider = cls._providers[provider_name](config)

        return provider.get_llm(purpose)