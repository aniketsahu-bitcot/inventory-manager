"""
FastAPI app that uses the SQLAlchemy models.
"""

from fastapi import FastAPI

app = FastAPI(title="Inventory API")

@app.get("/")
def root()->None:
    """Root endpoint to check API status."""
    return {"message": "Inventory API is running"}
