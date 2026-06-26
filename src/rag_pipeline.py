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


SIMILARITY_THRESHOLD = 1.2


def ask_question(
        question: str,
        vector_store
):
    logger.info(
        f"Question received: {question}"
    )

    retrieval_timer = Timer()
    retrieval_timer.start()

    retrieved_docs = (
        vector_store
        .similarity_search_with_score(
            question,
            k=3
        )
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
                "chunk_id": chunk_id,
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
You are a helpful assistant.

Answer ONLY from the supplied context.

Rules:

1. Do not use outside knowledge.
2. If the answer is unavailable, reply exactly:

I do not have enough information.

3. Be concise and factual.

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