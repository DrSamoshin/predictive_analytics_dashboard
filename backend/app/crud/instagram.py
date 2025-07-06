"""
CRUD operations for Instagram models.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.instagram import InstagramAccount, InstagramMedia
from app.schemas.instagram import (
    InstagramAccountCreate, 
    InstagramAccountUpdate,
    InstagramMediaCreate,
    InstagramMediaUpdate
)


class InstagramAccountCRUD:
    """CRUD operations for Instagram accounts."""

    @staticmethod
    async def get_by_id(db: AsyncSession, account_id: int) -> Optional[InstagramAccount]:
        """Get Instagram account by ID."""
        result = await db.execute(select(InstagramAccount).where(InstagramAccount.id == account_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> List[InstagramAccount]:
        """Get all Instagram accounts for a user."""
        result = await db.execute(
            select(InstagramAccount).where(InstagramAccount.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_instagram_user_id(db: AsyncSession, instagram_user_id: str) -> Optional[InstagramAccount]:
        """Get Instagram account by Instagram user ID."""
        result = await db.execute(
            select(InstagramAccount).where(InstagramAccount.instagram_user_id == instagram_user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_active_by_user_id(db: AsyncSession, user_id: int) -> Optional[InstagramAccount]:
        """Get active Instagram account for a user."""
        result = await db.execute(
            select(InstagramAccount).where(
                and_(
                    InstagramAccount.user_id == user_id,
                    InstagramAccount.is_active == True,
                    InstagramAccount.is_connected == True
                )
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_id: int, account_data: InstagramAccountCreate) -> InstagramAccount:
        """Create new Instagram account connection."""
        db_account = InstagramAccount(
            user_id=user_id,
            instagram_user_id=account_data.instagram_user_id,
            username=account_data.username,
            account_type=account_data.account_type,
            access_token=account_data.access_token,
            token_expires_at=account_data.token_expires_at
        )
        
        try:
            db.add(db_account)
            await db.commit()
            await db.refresh(db_account)
            return db_account
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, account_id: int, account_data: InstagramAccountUpdate) -> Optional[InstagramAccount]:
        """Update Instagram account."""
        result = await db.execute(select(InstagramAccount).where(InstagramAccount.id == account_id))
        db_account = result.scalar_one_or_none()
        
        if not db_account:
            return None
        
        update_data = account_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_account, field, value)
        
        db_account.updated_at = datetime.utcnow()
        
        try:
            await db.commit()
            await db.refresh(db_account)
            return db_account
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def update_token(db: AsyncSession, account_id: int, access_token: str, expires_at: Optional[datetime] = None) -> Optional[InstagramAccount]:
        """Update Instagram account token."""
        result = await db.execute(select(InstagramAccount).where(InstagramAccount.id == account_id))
        db_account = result.scalar_one_or_none()
        
        if not db_account:
            return None
        
        db_account.access_token = access_token
        db_account.token_expires_at = expires_at
        db_account.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_account)
        return db_account

    @staticmethod
    async def delete(db: AsyncSession, account_id: int) -> bool:
        """Delete Instagram account."""
        result = await db.execute(select(InstagramAccount).where(InstagramAccount.id == account_id))
        db_account = result.scalar_one_or_none()
        
        if not db_account:
            return False
        
        await db.delete(db_account)
        await db.commit()
        return True


class InstagramMediaCRUD:
    """CRUD operations for Instagram media."""

    @staticmethod
    async def get_by_id(db: AsyncSession, media_id: int) -> Optional[InstagramMedia]:
        """Get Instagram media by ID."""
        result = await db.execute(select(InstagramMedia).where(InstagramMedia.id == media_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_account_id(db: AsyncSession, account_id: int, limit: int = 25, offset: int = 0) -> List[InstagramMedia]:
        """Get Instagram media for an account."""
        result = await db.execute(
            select(InstagramMedia)
            .where(InstagramMedia.account_id == account_id)
            .order_by(InstagramMedia.published_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_instagram_media_id(db: AsyncSession, instagram_media_id: str) -> Optional[InstagramMedia]:
        """Get Instagram media by Instagram media ID."""
        result = await db.execute(
            select(InstagramMedia).where(InstagramMedia.instagram_media_id == instagram_media_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, media_data: InstagramMediaCreate) -> InstagramMedia:
        """Create new Instagram media."""
        db_media = InstagramMedia(**media_data.model_dump())
        
        try:
            db.add(db_media)
            await db.commit()
            await db.refresh(db_media)
            return db_media
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, media_id: int, media_data: InstagramMediaUpdate) -> Optional[InstagramMedia]:
        """Update Instagram media."""
        result = await db.execute(select(InstagramMedia).where(InstagramMedia.id == media_id))
        db_media = result.scalar_one_or_none()
        
        if not db_media:
            return None
        
        update_data = media_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_media, field, value)
        
        db_media.updated_at = datetime.utcnow()
        
        try:
            await db.commit()
            await db.refresh(db_media)
            return db_media
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def bulk_create_or_update(db: AsyncSession, media_items: List[InstagramMediaCreate]) -> List[InstagramMedia]:
        """Bulk create or update Instagram media items."""
        created_items = []
        
        for media_data in media_items:
            # Check if media already exists
            existing_media = await InstagramMediaCRUD.get_by_instagram_media_id(
                db, media_data.instagram_media_id
            )
            
            if existing_media:
                # Update existing media
                update_data = InstagramMediaUpdate(
                    like_count=media_data.like_count,
                    comments_count=media_data.comments_count,
                    caption=media_data.caption
                )
                updated_media = await InstagramMediaCRUD.update(db, existing_media.id, update_data)
                if updated_media:
                    created_items.append(updated_media)
            else:
                # Create new media
                new_media = await InstagramMediaCRUD.create(db, media_data)
                created_items.append(new_media)
        
        return created_items


# Create instances to use in endpoints
instagram_account_crud = InstagramAccountCRUD()
instagram_media_crud = InstagramMediaCRUD() 