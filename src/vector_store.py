from pathlib import Path
import json
from src.logger import logger

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter


EMBEDDING_MODEL = "all-MiniLM-L6-v2"

INDEX_PATH = "faiss_index"

METADATA_FILE = "faiss_index/indexed_files.json"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(
        documents
    )

    for index, chunk in enumerate(chunks):
        
        source_file = Path(chunk.metadata["source"]).name

        chunk.metadata["chunk_id"] = (f"{source_file}_{index}")

    return chunks


def vector_store_exists():

    return (
        Path(
            f"{INDEX_PATH}/index.faiss"
        ).exists()
        and
        Path(
            f"{INDEX_PATH}/index.pkl"
        ).exists()
    )


def load_vector_store():

    embeddings = get_embeddings()

    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def create_vector_store(documents):

    chunks = create_chunks(documents)

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(
        INDEX_PATH
    )

    return vector_store


def update_vector_store(documents):

    chunks = create_chunks(documents)

    indexed_files = set()

    metadata_path = Path(METADATA_FILE)

    if metadata_path.exists():

        with open(
                metadata_path,
                "r",
                encoding="utf-8"
        ) as file:

            indexed_files = set(
                json.load(file)
            )

    new_chunks = []

    for chunk in chunks:

        source = Path(
            chunk.metadata["source"]
        ).name

        if source not in indexed_files:

            new_chunks.append(
                chunk
            )
            
    if not new_chunks:
        
        logger.info("No new files found.")

        print(
            "\nNo new files found."
        )

        return load_vector_store()

    embeddings = get_embeddings()

    if vector_store_exists():

        vector_store = load_vector_store()

        vector_store.add_documents(
            new_chunks
        )

    else:

        vector_store = FAISS.from_documents(
            new_chunks,
            embeddings
        )

    vector_store.save_local(
        INDEX_PATH
    )
    logger.info("FAISS index saved.")

    indexed_files.update(

        Path(
            chunk.metadata["source"]
        ).name

        for chunk in new_chunks
    )

    with open(
            METADATA_FILE,
            "w",
            encoding="utf-8"
    ) as file:

        json.dump(
            list(indexed_files),
            file,
            indent=4
        )

    return vector_store