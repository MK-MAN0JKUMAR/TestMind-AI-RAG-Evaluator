from pathlib import Path
from src.logger import logger

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from src.llm import get_llm
from src.latency import Timer
from src.retrievers import RetrieverFactory

SIMILARITY_THRESHOLD = 1.5


def ask_question(
        question: str,
        vector_store
):
    logger.info(
        f"Question received: {question}"
    )

    retrieval_timer = Timer()
    retrieval_timer.start()

    retriever = RetrieverFactory.get_retriever(
        vector_store
    )

    retrieved_docs = retriever.retrieve(
        question=question,
        k=3
    )

    retrieval_latency = retrieval_timer.stop()

    if not retrieved_docs:

        return {
            "question": question,
            "answer": "No relevant information found.",
            "contexts": [],
            "sources": [],
            "retrieved_docs": [],
            "latency": {
                "retrieval": retrieval_latency,
                "llm": 0.0
            }
        }

    contexts = []

    sources = set()

    retrieved_results = []

    for doc, score in retrieved_docs:
        
        if score > SIMILARITY_THRESHOLD:
            continue

        source = Path(
            doc.metadata.get(
                "source",
                "Unknown"
            )
        ).name

        chunk_id = doc.metadata.get(
            "chunk_id",
            "Unknown"
        )
        
        file_name = doc.metadata.get(
            "file_name",
            source
        )

        file_type = doc.metadata.get(
            "file_type",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        chunk_index = doc.metadata.get(
            "chunk_index",
            "Unknown"
        )

        total_chunks = doc.metadata.get(
            "total_chunks",
            "Unknown"
        )

        contexts.append(

            f"""
Source: {source}
Chunk ID: {chunk_id}

{doc.page_content}
"""
        )

        sources.add(
            source
        )
        
        retrieved_results.append(
            {
                "source": source,
                "file_name": file_name,
                "file_type": file_type,
                "page": page,
                "chunk_id": chunk_id,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks,
                "score": round(
                    float(score),
                    4
                ),
                "content": doc.page_content
            }
        )

    if not contexts:

        return {
            "question": question,
            "answer": "No relevant information found in the supplied documents.",
            "contexts": [],
            "sources": [],
            "retrieved_docs": [],
            "latency": {
                "retrieval": retrieval_latency,
                "llm": 0.0
            }
        }

    context = "\n\n".join(
        contexts
    )

    template = """
    You are an AI assistant for Retrieval-Augmented Generation (RAG).

    Use ONLY the information provided in the Context.

    Instructions:

    - Read the entire context carefully before answering.
    - If the answer is explicitly or implicitly present in the context, answer it in your own words.
    - Do NOT say "I do not have enough information" if the context contains the answer.
    - Do NOT use outside knowledge.
    - If the answer truly does not exist in the context, reply exactly:

    I do not have enough information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    
    prompt = ChatPromptTemplate.from_template(
        template
    )

    llm = get_llm()

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    llm_timer = Timer()
    llm_timer.start()

    answer = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )
    
    llm_latency = llm_timer.stop()

    logger.info(
    f"Question answered successfully. Retrieved {len(retrieved_results)} chunks."
    )

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "sources": list(
            sources
        ),
        "retrieved_docs": retrieved_results,
        "latency": {
            "retrieval": retrieval_latency,
            "llm": llm_latency
        }
    }