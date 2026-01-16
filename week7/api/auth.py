"""User registration endpoint for FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from week7.schemas.user import UserCreate, UserOut
from week7.models.user import User
from week7.db.dependencies import get_db_session
from week7.auth.security import hash_password, verify_password
from week7.auth.jwt_handler import create_access_token
from week7.db.session import get_db
from week7.schemas.auth import LoginRequest
from fastapi.responses import JSONResponse
from week7.models.refresh_token import RefreshToken
from week7.auth.security import generate_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta
import hashlib

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db))-> JSONResponse:
    """Authenticate user and provide JWT access and refresh tokens."""
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})

    raw_refresh, hashed_refresh = generate_refresh_token()
    refresh_token_expires = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    db.add(
        RefreshToken(
            token_hash=hashed_refresh,
            user_id=user.id,
            expires_at=refresh_token_expires,
            revoked=False
        )
    )
    db.commit()

    response_body = {
        "access_token": access_token,
        "refresh_token": raw_refresh,
        "token_type": "bearer"
    }

    response = JSONResponse(content=response_body)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=30 * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=raw_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return response


@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db))-> JSONResponse:
    """Logout user by revoking refresh token and clearing cookies."""
    raw_token = request.cookies.get("refresh_token")
    if raw_token:
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        db.query(RefreshToken).filter(
            RefreshToken.token_hash == hashed_token
        ).update({"revoked": True})
        db.commit()

    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/refresh")
async def refresh_token(request: Request, db: Session = Depends(get_db))-> JSONResponse:
    """Refresh access and refresh tokens using a valid refresh token."""
    raw_token = request.cookies.get("refresh_token")
    if not raw_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hashed_token,
        RefreshToken.revoked.is_(False)
    ).first()

    if not token or token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    token.revoked = True
    new_raw, new_hash = generate_refresh_token()
    db.add(RefreshToken(
        token_hash=new_hash,
        user_id=token.user_id,
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    ))
    db.commit()

    access_token = create_access_token({"user_id": token.user_id})

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=30*60
    )
    response.set_cookie(
        key="refresh_token",
        value=new_raw,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS*24*60*60
    )
    return response


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db_session)
)-> UserOut:
    """Register a new user with hashed password."""

    existing_user = db.query(User).filter(
        or_(
            User.username == user_in.username,
            User.email == user_in.email
        )
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    hashed_password = hash_password(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        role="staff"  
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
