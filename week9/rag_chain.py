"""RAG chain construction for question answering over product inventory."""
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.vectorstores import PGVector
from week9.constants import OLLAMA_MODEL, HUGGINGFACE_EMBEDDING_MODEL, HUGGINGFACE_COLLECTION_NAME
from langchain_community.chat_models import ChatOllama as Ollama
from week7.models.user import User
from typing import List
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")
if not POSTGRES_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")



class AccessControlledRetriever(BaseRetriever):
    """Retriever with access control filtering."""
    vectorstore: PGVector
    user_id: int
    k: int = 12

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> List[Document]:
        
        """Retrieve documents with access control filtering."""

        docs = self.vectorstore.similarity_search(query, k=self.k)

        allowed_docs = []
        for doc in docs:
            meta = doc.metadata or {}

            if "product_id" in meta:
                allowed_docs.append(doc)

            elif meta.get("user_id") == self.user_id:
                allowed_docs.append(doc)

        return allowed_docs

def get_rag_chain(current_user: User)->Runnable[str,str]:

    """Build and return the RAG retriever and chain with access control."""
    vectorstore = PGVector(
        collection_name=HUGGINGFACE_COLLECTION_NAME,   
        connection_string=POSTGRES_URL,
        embedding_function=HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL),
    )

    llm = Ollama(model=OLLAMA_MODEL, temperature=0)

    retriever = AccessControlledRetriever(
        vectorstore=vectorstore,
        user_id=current_user.id,
        k=12,
    )

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

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

