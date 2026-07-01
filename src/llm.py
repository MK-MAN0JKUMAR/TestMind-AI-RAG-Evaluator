from src.evaluation_config import (
    ANSWER_PROVIDER,
    PROVIDERS,
)

from src.providers import LLMFactory


MODEL_NAME = PROVIDERS[ANSWER_PROVIDER]["answer"]["model"]


def get_llm():

    provider_config = PROVIDERS[ANSWER_PROVIDER]

    return LLMFactory.create(
        provider_name=ANSWER_PROVIDER,
        config=provider_config,
        purpose="answer",
    )