from src.retrievers.base import BaseRetriever


class FAISSRetriever(BaseRetriever):

    def __init__(
        self,
        vector_store
    ):
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
        k: int = 3
    ):
        return (
            self.vector_store
            .similarity_search_with_score(
                question,
                k=k
            )
        )