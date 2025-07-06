"""
Instagram integration models.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base


class InstagramAccount(Base):
    """Instagram account connection for users."""
    __tablename__ = "instagram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    instagram_user_id = Column(String(100), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False)
    account_type = Column(String(50), default="PERSONAL")  # PERSONAL, BUSINESS, CREATOR
    
    # Token information
    access_token = Column(Text, nullable=False)
    token_expires_at = Column(DateTime, nullable=True)
    
    # Account metadata
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_connected = Column(Boolean, default=True)
    last_sync_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="instagram_accounts")
    media_items = relationship("InstagramMedia", back_populates="account", cascade="all, delete-orphan")


class InstagramMedia(Base):
    """Instagram media posts data."""
    __tablename__ = "instagram_media"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("instagram_accounts.id"), nullable=False, index=True)
    instagram_media_id = Column(String(100), nullable=False, unique=True, index=True)
    
    # Media details
    media_type = Column(String(50), nullable=False)  # IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url = Column(Text, nullable=True)
    permalink = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    
    # Metrics
    like_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Timestamps  
    timestamp = Column(DateTime, nullable=True)  # Instagram post timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account = relationship("InstagramAccount", back_populates="media_items") 