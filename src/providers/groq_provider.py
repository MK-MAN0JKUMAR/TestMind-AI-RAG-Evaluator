import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.providers.base import BaseLLMProvider

load_dotenv()


class GroqProvider(BaseLLMProvider):

    def __init__(self, config):
        self.config = config

    def get_llm(self, purpose):

        settings = self.config[purpose]

        return ChatGroq(
            model=settings["model"],
            temperature=settings["temperature"],
            api_key=os.getenv(self.config["api_key_env"]),
        )