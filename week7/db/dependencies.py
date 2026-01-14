"""Database dependency utilities."""
from sqlalchemy.orm import Session
from week7.db.session import get_db
from fastapi import Depends

def get_db_session(db: Session = Depends(get_db))-> Session:
    """Dependency that provides a database session."""
    return db
