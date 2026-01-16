"""Security utilities for password hashing and verification."""
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import hashlib
from datetime import datetime

REFRESH_TOKEN_EXPIRE_DAYS = 7

def generate_refresh_token() -> tuple[str, str]:
    """Generate a secure refresh token and its hash."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, token_hash

def is_refresh_token_expired(expiry: datetime) -> bool:
    """Check if the refresh token is expired."""
    return datetime.utcnow() > expiry


def hash_password(password: str) -> str:
    """Hash password using PBKDF2 (no 72-byte limit, no bcrypt issues)"""
    return generate_password_hash(password, method='pbkdf2:sha256:600000')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return check_password_hash(hashed_password, plain_password)
