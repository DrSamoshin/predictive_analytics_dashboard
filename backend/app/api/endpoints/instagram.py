"""
Instagram integration endpoints.

CRITICAL WARNING: Instagram Basic Display API was deprecated on December 4, 2024.
This module provides limited functionality using existing database data only.
"""

import logging
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.instagram import (
    InstagramOAuthURL,
    InstagramOAuthCallback,
    InstagramAccountResponse,
    InstagramMediaResponse,
    InstagramUserProfile,
    InstagramAccountCreate
)
from app.crud.instagram import instagram_account_crud, instagram_media_crud
from app.services.instagram import instagram_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/auth/url", response_model=InstagramOAuthURL)
async def get_instagram_auth_url(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get Instagram OAuth authorization URL (DEPRECATED).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint is no longer functional.
    """
    logger.warning("Attempt to use deprecated Instagram Basic Display API")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Instagram Basic Display API was deprecated on December 4, 2024. "
               "New Instagram connections are no longer available. "
               "Please check INSTAGRAM_API_MIGRATION.md for migration options."
    )


@router.post("/auth/callback")
async def instagram_oauth_callback(
    callback_data: InstagramOAuthCallback,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Instagram OAuth callback (DEPRECATED).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint is no longer functional.
    """
    logger.warning("Attempt to use deprecated Instagram OAuth callback")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Instagram Basic Display API was deprecated on December 4, 2024. "
               "OAuth authorization is no longer available. "
               "Please check INSTAGRAM_API_MIGRATION.md for migration options."
    )


@router.get("/accounts", response_model=List[InstagramAccountResponse])
async def get_instagram_accounts(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's Instagram accounts (LIMITED FUNCTIONALITY).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint returns existing accounts from database but they are no longer connected.
    """
    logger.info(f"Fetching Instagram accounts for user {current_user.id} (deprecated API)")
    accounts = await instagram_account_crud.get_by_user_id(db, current_user.id)
    
    # Mark all accounts as disconnected since API is deprecated
    for account in accounts:
        account.is_connected = False
        account.is_active = False
    
    return accounts


@router.get("/accounts/{account_id}", response_model=InstagramAccountResponse)
async def get_instagram_account(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific Instagram account (LIMITED FUNCTIONALITY).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint returns existing account data but it is no longer connected.
    """
    account = await instagram_account_crud.get_by_id(db, account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # Mark account as disconnected since API is deprecated
    account.is_connected = False
    account.is_active = False
    
    return account


@router.delete("/accounts/{account_id}")
async def disconnect_instagram_account(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete Instagram account from database."""
    account = await instagram_account_crud.get_by_id(db, account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    success = await instagram_account_crud.delete(db, account_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete Instagram account"
        )
    
    logger.info(f"Deleted Instagram account {account_id} for user {current_user.id}")
    return {"message": "Instagram account deleted successfully"}


@router.post("/accounts/{account_id}/sync")
async def sync_instagram_data(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sync Instagram account data (DEPRECATED).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    Data synchronization is no longer available.
    """
    logger.warning(f"Attempt to sync deprecated Instagram account {account_id}")
    
    # Verify account ownership
    account = await instagram_account_crud.get_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Instagram Basic Display API was deprecated on December 4, 2024. "
               "Data synchronization is no longer available. Existing data remains in database. "
               "Please check INSTAGRAM_API_MIGRATION.md for migration options."
    )


@router.get("/accounts/{account_id}/media", response_model=List[InstagramMediaResponse])
async def get_instagram_media(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get Instagram media for account (HISTORICAL DATA ONLY).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint returns existing media from database but no new data can be fetched.
    """
    # Verify account ownership
    account = await instagram_account_crud.get_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # Get media from database only - no API calls possible
    media = await instagram_media_crud.get_by_account_id(
        db, account_id, limit=limit, offset=offset
    )
    
    logger.info(f"Retrieved {len(media)} historical Instagram media items for account {account_id}")
    return media


@router.get("/accounts/{account_id}/profile", response_model=InstagramUserProfile)
async def get_instagram_profile(
    account_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get Instagram user profile (HISTORICAL DATA ONLY).
    
    Instagram Basic Display API was deprecated on December 4, 2024.
    This endpoint returns cached profile data from database only.
    """
    # Verify account ownership
    account = await instagram_account_crud.get_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # Return cached profile data
    profile = InstagramUserProfile(
        id=account.instagram_user_id,
        username=account.username,
        account_type=account.account_type,
        media_count=account.media_count or 0
    )
    
    logger.info(f"Retrieved historical Instagram profile for account {account_id}")
    return profile 