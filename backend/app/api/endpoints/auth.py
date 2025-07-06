"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_active_user
from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """User registration endpoint."""
    
    # Check if user with email already exists
    if await user_crud.get_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if await user_crud.get_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    try:
        db_user = await user_crud.create(db, user_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user"
        )
    
    return UserResponse.model_validate(db_user)


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """User login endpoint."""
    
    # Find user by email or username
    user = await user_crud.get_by_login(db, credentials.login)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current user profile information."""
    return current_user


@router.post("/logout")
async def logout():
    """User logout endpoint."""
    # For JWT tokens, logout is handled on the client side
    # by simply removing the token from storage
    return {"message": "Successfully logged out"} 