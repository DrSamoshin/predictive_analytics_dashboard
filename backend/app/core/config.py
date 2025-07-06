"""
Configuration settings for the application.
"""

import os
from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Instagram Predictive Analytics Dashboard"
    
    # CORS
    ALLOWED_HOSTS: Union[str, List[str]] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/instagram_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Instagram Basic Display API
    INSTAGRAM_APP_ID: str = ""
    INSTAGRAM_APP_SECRET: str = ""
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:8000/api/v1/instagram/callback"
    
    # ML Model settings
    MODEL_UPDATE_INTERVAL_HOURS: int = 24
    PREDICTION_WINDOW_DAYS: int = 7
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @field_validator('ALLOWED_HOSTS', mode='before')
    @classmethod
    def assemble_allowed_hosts(cls, v) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return [str(v)]

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

settings = Settings() 