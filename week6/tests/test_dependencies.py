"""Tests for the database dependency in week6.db.dependencies."""
from week6.db.dependencies import get_db
from sqlalchemy.orm import Session


def test_get_db_yields_session()-> None:
    """Test that get_db dependency yields a SQLAlchemy Session instance."""
    
    db_gen = get_db()

    db = next(db_gen)
    assert isinstance(db, Session)

    db_gen.close()
