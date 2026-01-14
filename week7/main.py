"""Main application entry point for Authentication System."""
from fastapi import FastAPI
from week7.db.base import Base
from week7.db.session import engine
from week7.api.auth import router as auth_router
from week6.api.routes import router as products_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Manager", version="1.0.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["products"])

@app.get("/")
def read_root()-> dict:
    """Root endpoint providing basic info."""
    return {"message": "Authentication System"}
