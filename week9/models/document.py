"""Document model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from week7.db.base import Base


class Document(Base):
    """Document model representing uploaded text documents."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)         
    content_type = Column(String(100), default="text/plain")

    created_at = Column(DateTime, default=datetime.utcnow)
