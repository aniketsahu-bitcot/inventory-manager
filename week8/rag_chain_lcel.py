"""Build a RAG chain using LCEL for inventory product questions."""
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import PGVector
from week8.constants import Embedding_MODEL, COLLECTION_NAME, MODEL_NAME
from week8.create_vectorstore import POSTGRES_URL  



def build_rag_chain():
    """
    Build a full RAG chain using LCEL.
    """
    embeddings = OpenAIEmbeddings(
        model=Embedding_MODEL,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    vectorstore = PGVector(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

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

    rag_chain = (

        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }

        | prompt
        | model
        | StrOutputParser()
    )

    return rag_chain


if __name__ == "__main__":
    rag = build_rag_chain()
    answer = rag.invoke("Give all information about the product 'Mango'.")
    print("Answer:", answer)
