"""A simple chat application that interacts with a language model
and calculates the cost based on token usage."""

from openai import OpenAI
import os
from constants import (
    MODEL_NAME,
    INPUT_COST_PER_TOKEN,
    OUTPUT_COST_PER_TOKEN,
    SYSTEM_PROMPT,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat()-> None:
    """Interact with the language model and calculate cost based on token usage."""
    
    user_query = input("Enter your query: ")

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ],
        )
    except Exception as e:
        print("\n API Error:", e)
        return

    reply = response.choices[0].message.content

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = input_tokens + output_tokens

    cost = (
        input_tokens * INPUT_COST_PER_TOKEN +
        output_tokens * OUTPUT_COST_PER_TOKEN
    )

    print("\n--- Response ---")
    print(reply)

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
