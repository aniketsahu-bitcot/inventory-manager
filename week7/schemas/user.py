"""Pydantic schemas for user data validation and serialization."""
from pydantic import BaseModel, EmailStr
from pydantic import Field

class UserBase(BaseModel):
    """Base model for User with common fields."""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Model for creating a new User with password."""
    password: str = Field(
        ...,
        min_length=8,
        description="Minimum length of password should be 8 characters"
    )

class UserOut(UserBase):
    """Model for reading User data."""
    id: int
    role: str
    is_active: bool

    class Config:
        from_attributes = True
