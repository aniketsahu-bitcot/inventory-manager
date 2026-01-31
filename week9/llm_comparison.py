"""LLM Comparison Tool: Compare speed and quality of OpenAI vs Ollama models."""
import time
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from constants import OPENAI_MODEL, OLLAMA_MODEL

openai_llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=1
)

ollama_llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=1
)

def run_model(llm, model_name, prompt)-> dict:
    """Run the given LLM with the prompt and measure latency."""
    start_time = time.time()
    response = llm.invoke([HumanMessage(content=prompt)])
    end_time = time.time()

    return {
        "model": model_name,
        "response": response.content,
        "latency_seconds": round(end_time - start_time, 3)
    }

print("=== LLM SPEED & QUALITY COMPARATOR ===\n")
print("Type your prompt and press Enter. Type 'exit' to quit.\n")

while True:
    
    user_prompt = input("Your prompt: ").strip()
    
    
    if user_prompt.lower() in ['exit']:
        print("\nGoodbye!")
        break
    
    if not user_prompt:
        print("Please enter a valid prompt.\n")
        continue
    
    print("\n" + "="*60)
    print(f"Prompt: {user_prompt}")
    print("="*60)
    
    
    print("\nTesting OpenAI...")
    openai_result = run_model(openai_llm, "OpenAI", user_prompt)
    
    
    print("Testing Ollama...")
    ollama_result = run_model(ollama_llm, "Ollama (Local)", user_prompt)
    
    
    print("\n=== SPEED COMPARISON ===")
    print(f"OpenAI Latency  : {openai_result['latency_seconds']}s")
    print(f"Ollama Latency  : {ollama_result['latency_seconds']}s")
    
    print("\n=== RESPONSE QUALITY ===")
    print("\n--- OpenAI Response ---")
    print(openai_result["response"])
    
    print("\n--- Ollama Response ---")
    print(ollama_result["response"])
    print("\n" + "="*60 + "\n")
