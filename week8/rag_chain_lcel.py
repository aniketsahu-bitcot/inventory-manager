"""Build a RAG chain using LCEL for inventory product questions with exception handling and SOLID principles."""
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import PGVector
from week8.constants import Embedding_MODEL, COLLECTION_NAME, MODEL_NAME
from week8.create_vectorstore import POSTGRES_URL


def create_embeddings()-> OpenAIEmbeddings:
    """Create OpenAI embeddings with exception handling."""
    try:
        return OpenAIEmbeddings(
            model=Embedding_MODEL,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    except Exception as e:
        print(f"[Error] Initializing embeddings: {e}")
        return None


def create_vectorstore(embeddings)-> PGVector:
    """Initialize PGVector vectorstore."""
    try:
        return PGVector(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            connection_string=POSTGRES_URL
        )
    except Exception as e:
        print(f"[Error] Connecting to vectorstore: {e}")
        return None


def build_retriever(vectorstore, k=3)-> any:
    """Create a retriever from the vectorstore."""
    try:
        return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
    except Exception as e:
        print(f"[Error] Creating retriever: {e}")
        return None


def build_rag_chain()-> any:
    """Build a RAG chain using LCEL."""
    embeddings = create_embeddings()
    if embeddings is None:
        return None

    vectorstore = create_vectorstore(embeddings)
    if vectorstore is None:
        return None

    retriever = build_retriever(vectorstore)
    if retriever is None:
        return None

    prompt = ChatPromptTemplate.from_template(
        """You are an assistant for answering questions about inventory products.

        Answer the question using ONLY the provided context.
        If the answer is not present in the context, say "I don't know".

        Context:
        {context}

        Question:
        {question}
        """
    )

    model = ChatOpenAI(model=MODEL_NAME, temperature=1)

    try:
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | model 
            | StrOutputParser()
        )
        return rag_chain
    except Exception as e:
        print(f"[Error] Building RAG chain: {e}")
        return None


def query_rag_chain(rag_chain, query: str)-> str:
    """Invoke RAG chain safely with exception handling."""
    if rag_chain is None:
        print("[Error] RAG chain is not available.")
        return None

    try:
        answer = rag_chain.invoke(query)
        return answer
    except Exception as e:
        print(f"[Error] Invoking RAG chain: {e}")
        return None


if __name__ == "__main__":
    rag_chain = build_rag_chain()
    query = input("Enter your query: ")
    answer = query_rag_chain(rag_chain, query)
    if answer:
        print("Answer:", answer)
