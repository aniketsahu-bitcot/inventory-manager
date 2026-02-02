"""
LangChain RAG chat API endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from week9.schemas.request_model import ChatRequest
from week9.schemas.response_model import ChatResponse
from week7.models.user import User
from week7.api.dependencies import roles_required
from week9.rag_chain import get_rag_chain
from week9.cache import get_cached_answer, store_answer

router = APIRouter()

@router.post("/inventory", response_model=ChatResponse)
def chat_inventory(
    request: ChatRequest,
    current_user: User = Depends(roles_required("GET")),
) -> ChatResponse:
    """Handle chat requests related to inventory management."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
       
       retriever, chain = get_rag_chain()
    
       cached = get_cached_answer(request.question)
       if cached is not None:

        return ChatResponse(answer=cached.replace("\n", " ").strip())
    
       answer = chain.invoke(request.question)
       store_answer(request.question, answer)
    
       return ChatResponse(answer=answer.replace("\n", " ").strip())

    except Exception as e:
       
      raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")