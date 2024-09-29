import os
import shutil
from loguru import logger

from langchain_community.vectorstores import Chroma
from langchain_core.documents.base import Document

from .get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

def create_db():
    with open("bot/ai/dataset.txt", "r", encoding="utf-8") as f:
        data = f.read()

    chunks = [Document(i, metadata={"source": "text"}) for i in data.split("|") if i]
    for chunk in chunks:
        print(
            chunk.page_content, 
            "\n\n\n"
            )

    # Creating the DataBase
    if os.path.exists(CHROMA_PATH):
        try:
            shutil.rmtree(CHROMA_PATH)
        except OSError as e:
            logger.error(f"Error while deleting directory: {e.filename} - {e.strerror}.")
            
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=get_embedding_function(), 
        ids=[str(i) for i in range(len(chunks))],
        persist_directory=CHROMA_PATH,
    )