from src.retrievers.faiss_retriever import FAISSRetriever


class RetrieverFactory:

    @staticmethod
    def get_retriever(
        vector_store,
        strategy: str = "faiss"
    ):

        strategy = strategy.lower()

        if strategy == "faiss":
            return FAISSRetriever(
                vector_store
            )

        raise ValueError(
            f"Unsupported retrieval strategy: {strategy}"
        )