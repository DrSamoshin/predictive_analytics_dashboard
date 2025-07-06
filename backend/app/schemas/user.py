"""
Pydantic schemas for User model.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base User schema with common fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserInDB(UserBase):
    """Schema for user data from database."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Schema for user data in API responses."""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class UserLogin(BaseModel):
    """Schema for user login."""
    login: str  # Can be either email or username
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None 