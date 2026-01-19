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

