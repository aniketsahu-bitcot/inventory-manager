"""Create a vector store in PostgreSQL using PGVector with open-source embeddings"""
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from dotenv import load_dotenv
from week8.load_products import load_products
from week8.split_documents import split_documents
from week9.constants import HUGGINGFACE_EMBEDDING_MODEL
from week9.constants import HUGGINGFACE_COLLECTION_NAME

load_dotenv()


try:
    POSTGRES_URL = os.environ["DATABASE_URL"]
except KeyError:
    raise RuntimeError("DATABASE_URL environment variable is not set")

NEW_COLLECTION_NAME = HUGGINGFACE_COLLECTION_NAME

def create_vectorstore(documents: list[Document]) -> PGVector:
    """Create a PGVector vector store using sentence-transformers"""

    embeddings = HuggingFaceEmbeddings(
        model_name=HUGGINGFACE_EMBEDDING_MODEL
    )

    vectorstore = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=NEW_COLLECTION_NAME,
        connection_string=POSTGRES_URL,
        use_jsonb=True,
        
    )

    return vectorstore


if __name__ == "__main__":
    docs = load_products()
    chunks = split_documents(docs)

    print("Number of chunks to insert:", len(chunks))

    vs = create_vectorstore(chunks)
    print("New vectorstore created successfully with MiniLM embeddings!")
