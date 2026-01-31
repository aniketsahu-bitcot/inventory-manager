"""LLM Comparison Tool: OpenAI vs Ollama with RAG"""
import time
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from constants import OPENAI_MODEL, OLLAMA_MODEL, COLLECTION_NAME, Embedding_MODEL
from langchain_community.vectorstores import PGVector
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

try:
    POSTGRES_URL = os.getenv("DATABASE_URL")
except KeyError:
    raise RuntimeError("DATABASE_URL environment variable is not set")


try:
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
except KeyError:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")



openai_llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=1
)

ollama_llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=1
)


embeddings = OpenAIEmbeddings(model=Embedding_MODEL, openai_api_key=OPENAI_API_KEY)
    

vectorstore = PGVector(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        connection_string=POSTGRES_URL,
        use_jsonb=True
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 20})


def build_rag_chain(llm)-> tuple:
    """Build a RAG chain with the given LLM."""

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

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def run_rag(chain, model_name, query) -> dict:
    """Run the RAG chain and measure latency."""
    start_time = time.time()
    answer = chain.invoke(query)
    end_time = time.time()

    return {
        "model": model_name,
        "response": answer,
        "latency_seconds": round(end_time - start_time, 3)
    }


openai_rag_chain = build_rag_chain(openai_llm)
ollama_rag_chain = build_rag_chain(ollama_llm)


print("\n=== LLM SPEED & RAG COMPARISON TOOL ===")
print("Type your prompt and press Enter.")
print("Type 'exit' to quit.\n")

while True:

    user_prompt = input("Your prompt: ").strip()

    if user_prompt.lower() == "exit":
        print("\nGoodbye!")
        break

    if not user_prompt:
        print("Please enter a valid prompt.\n")
        continue

    print("\n" + "=" * 70)
    print(f"PROMPT: {user_prompt}")
    print("=" * 70)

    print("\n=== RAG PIPELINE TEST ===")

    print("\nTesting OpenAI RAG...")
    openai_rag = run_rag(openai_rag_chain, OPENAI_MODEL, user_prompt)

    print("Testing Ollama RAG...")
    ollama_rag = run_rag(ollama_rag_chain, OLLAMA_MODEL, user_prompt)

    print("\n--- RAG SPEED ---")
    print(f"OpenAI RAG Latency  : {openai_rag['latency_seconds']}s")
    print(f"Ollama RAG Latency  : {ollama_rag['latency_seconds']}s")

    print("\n--- OpenAI RAG Response ---")
    print(openai_rag["response"])

    print("\n--- Ollama RAG Response ---")
    print(ollama_rag["response"])

    print("\n" + "=" * 70 + "\n")
