"""User registration endpoint for FastAPI application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from week7.schemas.user import UserCreate, UserOut
from week7.models.user import User
from week7.db.dependencies import get_db_session
from week7.auth.security import hash_password

router = APIRouter()

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
