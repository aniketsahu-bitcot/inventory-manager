"""Main FastAPI application entry point."""
from fastapi import FastAPI
from week8.api.chat import router as chat_router
from week7.api.auth import router as auth_router     
from week7.api.routes import router as products_router  
from week7.core.config import validate_env
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Inventory Manager", version="1.0.0")


@app.on_event("startup")
def startup_event() -> None:
    """Validate environment variables on app startup."""
    validate_env()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root()-> dict:
    """Root endpoint providing basic info."""
    return {"message": "Welcome to the Inventory Manager API!"}
