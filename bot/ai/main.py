from loguru import logger

from langchain_chroma import Chroma

from .get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

def get_hint(query_text: str):
    logger.info(f"Query: {query_text}")
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    
    results = db.similarity_search_with_score(query_text, k=3)
    
    return [doc.page_content for doc, _ in results]