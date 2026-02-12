"API endpoint for handling inventory-related questions using RAG and caching."
from fastapi import APIRouter, Depends, HTTPException
from week7.api.dependencies import roles_required
from week7.models.user import User
from week9.schemas.request_model import ChatRequest
from week9.schemas.response_model import ChatResponse
from week9.cache import get_cached_answer, store_answer
import os
from dotenv import load_dotenv
from week9.rag_chain import get_rag_chain

router = APIRouter()

load_dotenv()

POSTGRES_URL = os.getenv("DATABASE_URL")
if not POSTGRES_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


@router.post("/inventory", response_model=ChatResponse)
def chat_inventory(
    request: ChatRequest,
    current_user: User = Depends(roles_required("GET")),
) -> ChatResponse:
    """Endpoint to handle inventory-related questions using RAG and caching."""

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        
        cached = get_cached_answer(
            request.question,
            current_user.id
        )
        if cached is not None:
            return ChatResponse(
                answer=cached.replace("\n", " ").strip()
            )

        
        chain = get_rag_chain(current_user)
        answer = chain.invoke(request.question)

        
        store_answer(
            request.question,
            answer,
            current_user.id
        )

        return ChatResponse(
            answer=answer.replace("\n", " ").strip()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}",
        )
