"""Main application entry point for Inventory Manager with JWT."""
from dotenv import load_dotenv
from fastapi import FastAPI
from week7.api.auth import router as auth_router     
from week7.api.routes import router as products_router  
from week7.core.config import validate_env

load_dotenv()

app = FastAPI(title="Inventory Manager", version="2.0.0")


@app.on_event("startup")
def startup_event() -> None:
    """Validate environment variables on app startup."""
    validate_env()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["products"])

@app.get("/")
def read_root()-> dict:
    """Root endpoint providing basic info."""
    return {"message": "Authentication System"}
