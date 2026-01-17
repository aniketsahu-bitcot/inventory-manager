"""User registration endpoint for FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from week7.schemas.user import UserCreate, UserOut
from week7.models.user import User
from week7.auth.security import create_access_token
from week7.db.session import get_db
from week7.schemas.auth import LoginRequest
from fastapi.responses import JSONResponse
from week7.auth.security import ACCESS_EXPIRE_MIN, REFRESH_EXPIRE_DAYS, create_refresh_token, verify_token
from week7.auth.security import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db))-> JSONResponse:
    """Authenticate user and provide JWT tokens in HttpOnly cookies."""
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    )

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=ACCESS_EXPIRE_MIN * 60
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60
    )

    return response


@router.post("/logout")
async def logout(request: Request) -> JSONResponse:
    """Logout user by clearing JWT cookies."""
    has_access = request.cookies.get("access_token")
    has_refresh = request.cookies.get("refresh_token")

    if not has_access and not has_refresh:
        message = "You were not logged in"
    else:
        message = "Logged out successfully"

    response = JSONResponse(content={"message": message})

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="strict"
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="strict"
    )

    return response

@router.post("/refresh")
def refresh_token(request: Request) -> JSONResponse:
    """Refresh access token using refresh token."""
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
       payload = verify_token(refresh_token, "refresh")
    except Exception:
       raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


    new_access_token = create_access_token(int(payload["sub"]))

    response = JSONResponse(content={"message": "Token refreshed"})

    response.set_cookie(
        "access_token",
        new_access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=ACCESS_EXPIRE_MIN * 60
    )

    return response


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db)
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
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )
