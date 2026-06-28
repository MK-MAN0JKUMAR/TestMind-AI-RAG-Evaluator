from pathlib import Path
from tempfile import NamedTemporaryFile

from src.logger import logger

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


def load_documents(folder_path: str):

    documents = []

    folder = Path(folder_path)

    for file_path in folder.iterdir():

        if file_path.suffix.lower() == ".txt":

            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

            documents.extend(
                loader.load()
            )

        elif file_path.suffix.lower() == ".pdf":

            loader = PyPDFLoader(
                str(file_path)
            )

            documents.extend(
                loader.load()
            )

    logger.info(
        f"Loaded {len(documents)} documents from '{folder_path}'."
    )

    return documents


def load_uploaded_documents(uploaded_files):

    documents = []

    failed_files = []

    loaded_files = 0

    temp_files = []

    for uploaded_file in uploaded_files:

        suffix = Path(
            uploaded_file.name
        ).suffix.lower()

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_path = temp_file.name

        temp_files.append(
            temp_path
        )

        if suffix == ".txt":

            loader = TextLoader(
                temp_path,
                encoding="utf-8"
            )

        elif suffix == ".pdf":

            loader = PyPDFLoader(
                temp_path
            )

        else:
            continue
        
        try:

            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = uploaded_file.name

            documents.extend(docs)
            
            loaded_files += 1

        except Exception as e:

            logger.error(
                f"Failed to load '{uploaded_file.name}': {e}"
            )
            
            failed_files.append(
                uploaded_file.name
            )

            continue
        

    logger.info(
        f"Loaded {loaded_files} uploaded file(s), producing {len(documents)} document page(s)."
    )

    return documents, loaded_files, failed_files