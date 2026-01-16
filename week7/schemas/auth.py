"""Authentication schemas."""
from pydantic import BaseModel

class LoginRequest(BaseModel):
    """Model for login request."""
    username: str
    password: str

class Token(BaseModel):
    """Model for JWT token response."""
    access_token: str
    token_type: str

class UserBase(BaseModel):
    """Base model for user."""
    username: str
    email: str

class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str
    role_id: int 

class UserRead(UserBase):
    """Model for reading user data."""
    id: int
    role: str
    
    class Config:
        """ORM mode for reading from database."""
        from_attributes = True

