"""
Instagram Basic Display API service.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import httpx
from urllib.parse import urlencode

from app.core.config import get_settings
from app.core.constants import (
    INSTAGRAM_ENDPOINTS,
    INSTAGRAM_BASIC_SCOPES,
    INSTAGRAM_DEFAULT_LIMIT,
    INSTAGRAM_TOKEN_EXPIRY_DAYS
)
from app.schemas.instagram import (
    InstagramUserProfile,
    InstagramMediaList,
    InstagramMediaItem,
    InstagramTokenResponse
)

logger = logging.getLogger(__name__)
settings = get_settings()


class InstagramAPIService:
    """Service for Instagram Basic Display API integration."""

    def __init__(self):
        self.app_id = settings.INSTAGRAM_APP_ID
        self.app_secret = settings.INSTAGRAM_APP_SECRET
        self.redirect_uri = settings.INSTAGRAM_REDIRECT_URI

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate Instagram OAuth authorization URL."""
        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "scope": ",".join(INSTAGRAM_BASIC_SCOPES),
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
        
        url = f"{INSTAGRAM_ENDPOINTS['authorize']}?{urlencode(params)}"
        logger.info(f"Generated Instagram authorization URL for app_id: {self.app_id}")
        return url

    async def exchange_code_for_token(self, code: str) -> InstagramTokenResponse:
        """Exchange authorization code for access token."""
        data = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    INSTAGRAM_ENDPOINTS["token"],
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                token_data = response.json()
                
                logger.info(f"Successfully exchanged code for token for user: {token_data.get('user_id')}")
                return InstagramTokenResponse(**token_data)
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to exchange code for token: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    async def get_long_lived_token(self, short_lived_token: str) -> Dict[str, Any]:
        """Exchange short-lived token for long-lived token."""
        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.app_secret,
            "access_token": short_lived_token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{INSTAGRAM_ENDPOINTS['user_profile']}/access_token",
                    params=params
                )
                response.raise_for_status()
                token_data = response.json()
                
                logger.info("Successfully exchanged for long-lived token")
                return token_data
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get long-lived token: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    async def refresh_token(self, access_token: str) -> Dict[str, Any]:
        """Refresh long-lived access token."""
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": access_token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{INSTAGRAM_ENDPOINTS['user_profile']}/refresh_access_token",
                    params=params
                )
                response.raise_for_status()
                token_data = response.json()
                
                logger.info("Successfully refreshed access token")
                return token_data
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    async def get_user_profile(self, access_token: str) -> InstagramUserProfile:
        """Get Instagram user profile information."""
        params = {
            "fields": "id,username,account_type,media_count",
            "access_token": access_token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    INSTAGRAM_ENDPOINTS["user_profile"],
                    params=params
                )
                response.raise_for_status()
                profile_data = response.json()
                
                logger.info(f"Successfully retrieved profile for user: {profile_data.get('username')}")
                return InstagramUserProfile(**profile_data)
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get user profile: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    async def get_user_media(
        self, 
        access_token: str, 
        limit: int = INSTAGRAM_DEFAULT_LIMIT,
        after: Optional[str] = None
    ) -> InstagramMediaList:
        """Get Instagram user media posts."""
        params = {
            "fields": "id,media_type,media_url,permalink,caption,timestamp",
            "access_token": access_token,
            "limit": limit
        }
        
        if after:
            params["after"] = after

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    INSTAGRAM_ENDPOINTS["user_media"],
                    params=params
                )
                response.raise_for_status()
                media_data = response.json()
                
                logger.info(f"Successfully retrieved {len(media_data.get('data', []))} media items")
                return InstagramMediaList(**media_data)
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get user media: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    async def get_media_details(self, media_id: str, access_token: str) -> InstagramMediaItem:
        """Get details for a specific media item."""
        params = {
            "fields": "id,media_type,media_url,permalink,caption,timestamp",
            "access_token": access_token
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{INSTAGRAM_ENDPOINTS['media_details']}/{media_id}",
                    params=params
                )
                response.raise_for_status()
                media_data = response.json()
                
                logger.info(f"Successfully retrieved media details for: {media_id}")
                return InstagramMediaItem(**media_data)
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get media details for {media_id}: {str(e)}")
            raise Exception(f"Instagram API error: {str(e)}")

    def calculate_token_expiry(self, expires_in_seconds: int) -> datetime:
        """Calculate token expiry date."""
        return datetime.utcnow() + timedelta(seconds=expires_in_seconds)

    def is_token_expiring_soon(self, expires_at: datetime, threshold_days: int = 7) -> bool:
        """Check if token is expiring within threshold days."""
        if not expires_at:
            return False
        return expires_at <= datetime.utcnow() + timedelta(days=threshold_days)


# Create service instance
instagram_service = InstagramAPIService() 