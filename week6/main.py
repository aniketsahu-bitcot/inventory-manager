"""
This module defines a FastAPI application with a root endpoint
that responds with a JSON greeting message.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Handle GET requests to the root URL ("/") and respond
    with a simple greeting message in JSON format.
    """
    return {"Hello": "World!"}
