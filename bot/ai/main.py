from loguru import logger

from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_chroma import Chroma

from .get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
ТыТы являешься технической поддержкой сервиса RuTube. 
Соответственно ты не должен отвечать на те вопросы, которые не касаются твоей сферы деятельности. 
Если тебе зададут вопрос, который тебя не касается, проси прощения упользователя 
и попроси его задать вопрос про техническую проблему."
Ответьте на вопрос, основываясь только на следующем контексте:

{context}

---

Ответьте на вопрос, основываясь на вышеприведенном контексте: {question},
"""

def get_hint(query_text: str):
    logger.info(f"Query: {query_text}")
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    
    results = db.similarity_search_with_score(query_text, k=3)    
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    
    llm = Ollama(
        model="llama3.1:8b",
        temperature=3
    )
    response_text = llm.invoke(prompt)
    
    return response_text