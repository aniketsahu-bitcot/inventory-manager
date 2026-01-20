"""SQLAlchemy model for the User entity."""
from sqlalchemy import Column, Integer, String, ForeignKey
from week7.db.base import Base
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

class User(Base):
    """Represents a user in the system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = Column(String(50), nullable=False, default="staff")
    role_ref = relationship("Role")
    is_active = Column(Boolean, default=True, nullable=False)
