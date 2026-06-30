from langchain_ollama import ChatOllama

from src.evaluation_config import ANSWER


MODEL_NAME = ANSWER["model"]


def get_llm():

    return ChatOllama(
        model=ANSWER["model"],
        temperature=ANSWER["temperature"]
    )