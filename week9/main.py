"""
Main FastAPI application entry point.

LLM caching with LangChain + SQLAlchemy + Alembic.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from week9.api.chat import router as chat_router
from week7.api.auth import router as auth_router
from week7.api.routes import router as products_router
from week7.core.config import validate_env
import langchain
langchain.debug = True
langchain.verbose = True

load_dotenv()

app = FastAPI(
    title="Inventory Manager – Week 9",
    version="1.1.0",
    description="Inventory RAG with LangChain LLM caching",
)


@app.on_event("startup")
def startup_event() -> None:
    """
    Application startup logic.
    """
    validate_env()


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])


@app.get("/")
def read_root() -> dict:
    """
    Root health endpoint.
    """
    return {
        "message": "Inventory Manager API (Week 9 – LLM Caching Enabled)"
    }
