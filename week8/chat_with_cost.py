"""A simple chat application that interacts with a language model
and calculates the cost based on token usage using LangChain."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from constants import (
    MODEL_NAME,
    INPUT_COST_PER_TOKEN,
    OUTPUT_COST_PER_TOKEN,
    SYSTEM_PROMPT,
)



def chat()-> None:
    """Interact with the language model and calculate cost based on token usage."""
    
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=MODEL_NAME,
        temperature=1
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "{query}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    user_query = input("Enter your query: ")

    try:
        response = chain.invoke({"query": user_query})
        
        input_tokens = llm.get_num_tokens(user_query)
        output_tokens = llm.get_num_tokens(response)
        total_tokens = input_tokens + output_tokens

        cost = (
            input_tokens * INPUT_COST_PER_TOKEN +
            output_tokens * OUTPUT_COST_PER_TOKEN
        )

    except Exception as e:
        print("\nAPI Error:", e)
        return

    print("\n--- Response ---")
    print(response)

    print("\n--- Model Used ---")
    print(MODEL_NAME)

    print("\n--- Token Usage ---")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {total_tokens}")

    print("\n--- Cost ---")
    print(f"Estimated cost: ${cost:.6f}")


if __name__ == "__main__":
    chat()
