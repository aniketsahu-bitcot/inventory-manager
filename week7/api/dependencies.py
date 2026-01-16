"""Dependencies for FastAPI routes."""
from fastapi import Request, HTTPException
from week7.auth.security import verify_token

def get_current_user(request: Request)-> str:
    """Dependency to get the current authenticated user from the access token."""
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_token(token, "access")
    return payload["sub"]
