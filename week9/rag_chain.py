"""LangChain RAG chain with PostgreSQL vector store and LLM caching."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models.ollama import ChatOllama
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
import os
from week9.constants import OLLAMA_MODEL, Embedding_MODEL, COLLECTION_NAME
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from week7.db.session import engine 
from langchain_community.cache import FullLLMCache
from typing import Optional

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")

def _get_cache_key(question: str) -> str:
    """Deterministic key: normalize question"""
    return f"{question.strip().lower()}"  

def get_cached_answer(question: str) -> Optional[str]:
    """Retrieve cached answer if available from the default full_llm_cache table."""

    key = _get_cache_key(question)

    with Session(engine) as session:
        
        entry = session.query(FullLLMCache).filter_by(
            prompt=key,          
            llm=OLLAMA_MODEL
        ).order_by(FullLLMCache.idx.asc()).first()
        
        return entry.response if entry else None

def store_answer(question: str, answer: str) -> None:
    """Store the new answer in the default full_llm_cache table."""
    
    key = _get_cache_key(question)

    with Session(engine) as session:
        entry = FullLLMCache(
            prompt=key,
            llm=OLLAMA_MODEL,
            idx=0,
            response=answer
        )
        session.add(entry)
        session.commit()

def build_rag_chain()-> tuple:
    """Build and return the RAG chain and retriever."""
    embeddings = OpenAIEmbeddings(model=Embedding_MODEL, openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    vectorstore = PGVector(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL,
        use_jsonb=True
    )
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})  

    llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)


    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful inventory assistant. Answer using only the provided context.
        If you don't know or the info is not in the context, say "I don't have that information".
        
        IMPORTANT RULES:
        - Do NOT use markdown
        - Do NOT use bullet points
        - Do NOT use special characters like *, -, or **
        - Respond in plain text only

        Context:
        {context}"""),
        
        ("human", "{question}")
    ])

    def format_docs(docs)-> str:
        """Format retrieved documents into a context string."""
        return "\n\n".join(f"Product: {d.page_content}" for d in docs) 

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return retriever, chain

