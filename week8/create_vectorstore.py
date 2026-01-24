"""Create a vector store in PostgreSQL using PGVector for product embeddings."""
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from week8.constants import Embedding_MODEL, COLLECTION_NAME
from dotenv import load_dotenv
from load_products import load_products
from split_documents import split_documents

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")

def create_vectorstore(documents: list[Document]):
    """Create a PGVector vector store from product documents.""" 
    
    embeddings = OpenAIEmbeddings(
        model=Embedding_MODEL,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    vectorstore = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=POSTGRES_URL,
    )

    return vectorstore


if __name__ == "__main__":
    
    docs = load_products()

    chunks = split_documents(docs)

    print("Number of chunks to insert:", len(chunks))

    vs = create_vectorstore(chunks)
    print("Vectorstore created successfully!")
