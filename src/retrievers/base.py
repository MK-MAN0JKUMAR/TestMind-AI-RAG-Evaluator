from abc import ABC, abstractmethod


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        question: str,
        k: int = 3
    ):
        """
        Retrieve relevant documents.
        """
        pass