"""
Pydantic schema for chat endpoints.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request body for inventory chat endpoint.
    """
    question: str = Field(
        ...,
        min_length=1,
        description="User question about inventory products",
        example="What is the price of the laptop?",
    )