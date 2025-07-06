"""
CRUD operations for User model.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserCRUD:
    """CRUD operations for User model."""

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username."""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_login(db: AsyncSession, login: str) -> Optional[User]:
        """Get user by email or username."""
        result = await db.execute(
            select(User).where(
                (User.email == login) | (User.username == login)
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        """Create new user."""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user."""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        try:
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except IntegrityError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Delete user."""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return False
        
        await db.delete(db_user)
        await db.commit()
        return True

    @staticmethod
    async def activate(db: AsyncSession, user_id: int) -> Optional[User]:
        """Activate user account."""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        db_user.is_active = True
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def deactivate(db: AsyncSession, user_id: int) -> Optional[User]:
        """Deactivate user account."""
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        db_user.is_active = False
        await db.commit()
        await db.refresh(db_user)
        return db_user


# Create instance to use in endpoints
user_crud = UserCRUD() 