"""SQLAlchemy model for refresh tokens."""
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from week7.db.base import Base
from datetime import datetime

class RefreshToken(Base):
    """Model representing a refresh token."""
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
