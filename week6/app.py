"""
Main FastAPI application entry point.

This module creates the FastAPI app instance and includes the API router that exposes the inventory endpoints.
It integrates the existing `inventory_manager` package which handles all inventory operations.
"""

from fastapi import FastAPI
from week6.api.routes import router

app = FastAPI()

app.include_router(
    router,
    prefix="/api",
    tags=["Products"]
)


