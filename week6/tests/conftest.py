"""Pytest configuration for FastAPI integration tests using PostgreSQL."""

import pytest
from typing import Any
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from week6.main import app
from week6.db.base import Base
from week6.db.dependencies import get_db
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")



engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@contextmanager
def db_transaction() -> Any:
    """
    Open a transaction for a test and roll it back afterwards.
    This makes the database temporary per test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    except SQLAlchemyError:
        transaction.rollback()
        raise
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="session")
def setup_database() -> Any:
    """
    Create tables once for the test session and drop them at the end.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_database) -> Any:
    """
    Provide a database session wrapped in a rollback transaction.
    """
    with db_transaction() as session:
        yield session


@pytest.fixture()
def client(db_session: Session) -> Any:
    """
    FastAPI TestClient with PostgreSQL test database.
    """

    def override_get_db() -> Any:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
