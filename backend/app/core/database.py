"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Create declarative base for models
Base = declarative_base()


# Create async engine for PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.LOG_LEVEL == "DEBUG",
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """
    Dependency to get database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 