from langchain_ollama import ChatOllama

from src.providers.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self, config):
        self.config = config

    def get_llm(self, purpose):

        settings = self.config[purpose]

        return ChatOllama(
            model=settings["model"],
            temperature=settings["temperature"],
        )