"""Role model definition."""
from sqlalchemy import Column, Integer, String
from week7.db.base import Base

class Role(Base):
    """Role model representing user roles in the system."""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


