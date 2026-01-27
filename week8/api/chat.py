"""Chat API routes for inventory RAG-based question answering."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from week8.rag_chain_lcel import build_rag_chain, query_rag_chain

router = APIRouter(prefix="/chat", tags=["Chat"])

rag_chain = None


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str


def get_rag_chain()-> any:
    """
    Initialize RAG chain lazily and cache it on the function itself.
    """
    if not hasattr(get_rag_chain, "rag_chain"):
        chain = build_rag_chain()

        if chain is None:
            raise RuntimeError(
                "RAG chain initialization failed. "
                "Check OPENAI_API_KEY, database connection, and pgvector setup."
            )

        get_rag_chain.rag_chain = chain

    return get_rag_chain.rag_chain

@router.post("/inventory", response_model=ChatResponse)
def chat_inventory(request: ChatRequest) -> ChatResponse:
    """
    Ask questions about inventory products using RAG.
    """
    if not request.question.strip():
        
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        chain = get_rag_chain()
        answer = query_rag_chain(chain, request.question)

        if answer is None:
            raise RuntimeError("RAG chain returned no answer")

        return ChatResponse(answer=answer.replace("\n", " ").strip())

    except RuntimeError as e:

        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}",
        )
