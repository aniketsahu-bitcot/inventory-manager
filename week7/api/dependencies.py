"""Dependency to get the current authenticated user based on JWT token.
"""
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from week7.db.session import get_db
from week7.models.user import User
from week7.auth.jwt_handler import verify_token


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Retrieve the current authenticated user from the JWT token."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    payload = verify_token(token)
    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
