"""
Database dependencies for FastAPI endpoints.
"""

from typing import Any
from week6.db.session import SessionLocal


def get_db() -> Any:
    """
    FastAPI dependency that provides a SQLAlchemy database session.
    The session is closed automatically after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
