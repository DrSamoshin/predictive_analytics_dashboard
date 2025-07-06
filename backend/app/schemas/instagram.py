"""
Pydantic schemas for Instagram integration.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


# Instagram Account Schemas
class InstagramAccountBase(BaseModel):
    """Base Instagram account schema."""
    instagram_user_id: str
    username: str
    account_type: str = "PERSONAL"


class InstagramAccountCreate(InstagramAccountBase):
    """Schema for creating Instagram account connection."""
    access_token: str
    token_expires_at: Optional[datetime] = None


class InstagramAccountUpdate(BaseModel):
    """Schema for updating Instagram account."""
    username: Optional[str] = None
    account_type: Optional[str] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    media_count: Optional[int] = None
    is_active: Optional[bool] = None
    is_connected: Optional[bool] = None
    last_sync_at: Optional[datetime] = None


class InstagramAccountResponse(InstagramAccountBase):
    """Schema for Instagram account in API responses."""
    id: int
    user_id: int
    followers_count: int
    following_count: int
    media_count: int
    is_active: bool
    is_connected: bool
    last_sync_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# Instagram Media Schemas
class InstagramMediaBase(BaseModel):
    """Base Instagram media schema."""
    instagram_media_id: str
    media_type: str
    media_url: Optional[str] = None
    permalink: Optional[str] = None
    caption: Optional[str] = None


class InstagramMediaCreate(InstagramMediaBase):
    """Schema for creating Instagram media."""
    account_id: int
    like_count: int = 0
    comments_count: int = 0
    timestamp: Optional[datetime] = None


class InstagramMediaUpdate(BaseModel):
    """Schema for updating Instagram media."""
    like_count: Optional[int] = None
    comments_count: Optional[int] = None
    caption: Optional[str] = None


class InstagramMediaResponse(InstagramMediaBase):
    """Schema for Instagram media in API responses."""
    id: int
    account_id: int
    like_count: int
    comments_count: int
    timestamp: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# Instagram API Response Schemas
class InstagramUserProfile(BaseModel):
    """Schema for Instagram user profile from API."""
    id: str
    username: str
    account_type: Optional[str] = None
    media_count: Optional[int] = None


class InstagramMediaItem(BaseModel):
    """Schema for Instagram media item from API."""
    id: str
    media_type: str
    media_url: Optional[str] = None
    permalink: Optional[str] = None
    caption: Optional[str] = None
    timestamp: Optional[str] = None


class InstagramMediaList(BaseModel):
    """Schema for Instagram media list from API."""
    data: List[InstagramMediaItem]
    paging: Optional[dict] = None


# OAuth Schemas
class InstagramOAuthURL(BaseModel):
    """Schema for Instagram OAuth authorization URL."""
    authorization_url: str


class InstagramOAuthCallback(BaseModel):
    """Schema for Instagram OAuth callback."""
    code: str
    state: Optional[str] = None


class InstagramTokenResponse(BaseModel):
    """Schema for Instagram token response."""
    access_token: str
    user_id: str 