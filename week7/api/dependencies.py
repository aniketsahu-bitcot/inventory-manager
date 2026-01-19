"""Dependencies for FastAPI routes."""
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from week7.auth.security import verify_token
from week7.db.session import get_db
from week7.models.user import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get the current authenticated user from the access token."""
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
       payload = verify_token(token, "access")
    except Exception:
      raise HTTPException(status_code=401, detail="Invalid or expired access token")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user
