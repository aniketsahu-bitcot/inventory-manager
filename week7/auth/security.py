"""Security utilities for password hashing and JWT token management."""
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash


ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = 30
REFRESH_EXPIRE_DAYS = 7


def get_secret_key() -> str:
    """
    Fetch and validate JWT secret key at runtime.
    """
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY is not set")
    return secret

def create_access_token(user_id: int) -> str:
    """Create JWT access token."""
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MIN),
    }
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token."""
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS),
    }
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)


def verify_token(token: str, expected_type: str) -> dict:
    """Verify JWT token and its type."""
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])

        if payload.get("type") != expected_type:
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    """Hash password using PBKDF2."""
    return generate_password_hash(password, method="pbkdf2:sha256:600000")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return check_password_hash(hashed_password, plain_password)