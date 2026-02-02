"""RAG chain construction for question answering over product inventory."""
import os
from typing import Tuple
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.vectorstores.pgvector import PGVector
from langchain_community.chat_models import ChatOllama
from week9.constants import OLLAMA_MODEL, HUGGINGFACE_EMBEDDING_MODEL, HUGGINGFACE_COLLECTION_NAME

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")
if not POSTGRES_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


def build_rag_chain() -> Tuple[PGVector, object]:
    """
    Build and return the RAG retriever and chain.
    Returns:
        retriever: The vector store retriever
        chain: The runnable chain for question answering
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=HUGGINGFACE_EMBEDDING_MODEL
    )

    vectorstore = PGVector(
        collection_name=HUGGINGFACE_COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL,
        use_jsonb=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 20}
    )

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

    def format_docs(docs) -> str:
        """Format retrieved documents into a string."""
        return "\n\n".join(f"Product: {d.page_content}" for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return retriever, chain

def get_rag_chain()-> tuple:
    """Singleton pattern to get or create the RAG chain and retriever."""
    if not hasattr(get_rag_chain, "chain"):
        retriever, chain = build_rag_chain()
        get_rag_chain.retriever = retriever
        get_rag_chain.chain = chain
    return get_rag_chain.retriever, get_rag_chain.chain

