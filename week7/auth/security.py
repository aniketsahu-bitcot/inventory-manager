"""Security utilities for password hashing and verification."""
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash password using PBKDF2 (no 72-byte limit, no bcrypt issues)"""
    return generate_password_hash(password, method='pbkdf2:sha256:600000')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return check_password_hash(hashed_password, plain_password)
