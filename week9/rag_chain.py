"""LangChain RAG chain with PostgreSQL vector store and LLM caching."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
import os
from week9.constants import MODEL_NAME, Embedding_MODEL, COLLECTION_NAME
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from week7.db.session import engine 
from langchain_community.cache import FullLLMCache
from typing import Optional

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")

def _get_cache_key(question: str, context: str) -> str:
    """Deterministic key: normalize question + top context snippet"""
    return f"{question.strip().lower()} | {context[:500]}"  

def get_cached_answer(question: str) -> Optional[str]:
    """Retrieve cached answer if available from the default full_llm_cache table."""
    
    embeddings = OpenAIEmbeddings(
        model=Embedding_MODEL,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    vectorstore = PGVector(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 200}   
                                
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    key = _get_cache_key(question, context)

    with Session(engine) as session:
        
        entry = session.query(FullLLMCache).filter_by(
            prompt=key,          
            llm=MODEL_NAME
        ).order_by(FullLLMCache.idx.asc()).first()
        
        return entry.response if entry else None

def store_answer(question: str, answer: str) -> None:
    """Store the new answer in the default full_llm_cache table."""
    
    embeddings = OpenAIEmbeddings(
        model=Embedding_MODEL,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    vectorstore = PGVector(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 200}   
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    key = _get_cache_key(question, context)

    with Session(engine) as session:
        entry = FullLLMCache(
            prompt=key,
            llm=MODEL_NAME,
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
        connection_string=POSTGRES_URL
    )
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 200})  

    llm = ChatOpenAI(model=MODEL_NAME, temperature=1, cache=False)  

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful inventory assistant. Answer using only the provided context.
        If you don't know or the info is not in the context, say "I don't have that information".

        Context:
        {context}

        Use markdown formatting when helpful."""),
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

