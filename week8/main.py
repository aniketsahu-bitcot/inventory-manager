"""Main FastAPI application entry point."""
from fastapi import FastAPI
from week8.api.chat import router as chat_router

app = FastAPI(
    title="Inventory RAG API",
    description="Ask questions about inventory products using RAG",
    version="1.0.0",
)

app.include_router(chat_router)


@app.get("/")
def health_check()-> dict:
    """Status check endpoint."""
    return {"status": "ok"}

