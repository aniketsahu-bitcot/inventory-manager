"""
SQLAlchemy declarative base.

All ORM models must inherit from this Base so that Alembic
can correctly discover tables and generate migrations.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass
