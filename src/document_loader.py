from pathlib import Path
from src.logger import logger

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


def load_documents(folder_path: str):

    documents = []

    folder = Path(folder_path)

    for file_path in folder.iterdir():

        if file_path.suffix == ".txt":

            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

            documents.extend(
                loader.load()
            )
            
        elif file_path.suffix == ".pdf":

            loader = PyPDFLoader(
                str(file_path)
            )

            documents.extend(
                loader.load()
            )
                        
    return documents