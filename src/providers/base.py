from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def get_llm(self, purpose):
        pass