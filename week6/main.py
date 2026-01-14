"""
FastAPI app that uses the SQLAlchemy models.
"""

from fastapi import FastAPI
from week6.api.routes import router as product_router

app = FastAPI(title="Inventory API")

app.include_router(product_router, prefix="/api")

@app.get("/")
def root()->None:
    """Root endpoint to check API status."""
    return {"message": "Inventory API is running"}
