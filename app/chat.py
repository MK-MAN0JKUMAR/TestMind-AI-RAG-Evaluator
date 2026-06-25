from src.document_loader import (
    load_documents
)

from src.vector_store import (
    create_vector_store,
    load_vector_store,
    vector_store_exists
)

from src.rag_pipeline import (
    ask_question
)


DOCUMENT_FOLDER = "documents"


if vector_store_exists():

    print(
        "\nLoading existing FAISS index..."
    )

    vector_store = load_vector_store()

else:

    print(
        "\nCreating FAISS index..."
    )

    documents = load_documents(
        DOCUMENT_FOLDER
    )

    vector_store = create_vector_store(
        documents
    )


print(
    "\nSystem Ready."
)


while True:

    question = input(
        "\nAsk a question (exit to quit): "
    )

    if question.lower() == "exit":

        break

    result = ask_question(
        question,
        vector_store
    )

    print(
        "\nAnswer:\n"
    )

    print(
        result["answer"]
    )

    if result["sources"]:

        print(
            "\nSources:"
        )

        for source in result["sources"]:

            print(
                f"- {source}"
            )

    print(
        "\nRetrieved Chunks:"
    )

    for doc in result["retrieved_docs"]:

        print(
            f"""
Source : {doc['source']}
Score  : {doc['score']:.4f}

Content:
{doc['content']}
"""
        )