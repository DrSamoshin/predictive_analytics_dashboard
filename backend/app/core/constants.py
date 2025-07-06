"""
Application constants for Instagram integration and other services.
"""

# Instagram Basic Display API Constants
INSTAGRAM_API_BASE_URL = "https://graph.instagram.com"
INSTAGRAM_OAUTH_BASE_URL = "https://api.instagram.com/oauth"
INSTAGRAM_API_VERSION = "v21.0"

# Instagram OAuth Scopes
INSTAGRAM_BASIC_SCOPES = [
    "user_profile",
    "user_media"
]

# Instagram API Endpoints
INSTAGRAM_ENDPOINTS = {
    "authorize": f"{INSTAGRAM_OAUTH_BASE_URL}/authorize",
    "token": f"{INSTAGRAM_OAUTH_BASE_URL}/access_token",
    "user_profile": f"{INSTAGRAM_API_BASE_URL}/me",
    "user_media": f"{INSTAGRAM_API_BASE_URL}/me/media",
    "media_details": f"{INSTAGRAM_API_BASE_URL}",  # + media_id
}

# Instagram Media Types
INSTAGRAM_MEDIA_TYPES = {
    "IMAGE": "IMAGE",
    "VIDEO": "VIDEO",
    "CAROUSEL_ALBUM": "CAROUSEL_ALBUM"
}

# Pagination limits
INSTAGRAM_DEFAULT_LIMIT = 25
INSTAGRAM_MAX_LIMIT = 100

# Token refresh settings
INSTAGRAM_TOKEN_REFRESH_THRESHOLD_DAYS = 7  # Refresh token if expires within 7 days
INSTAGRAM_TOKEN_EXPIRY_DAYS = 60  # Instagram tokens expire in 60 days 