"""
Models package initialization.
Import all models here to ensure they are registered with SQLAlchemy.
"""

from app.models.user import User
from app.models.instagram import InstagramAccount, InstagramMedia

__all__ = ["User", "InstagramAccount", "InstagramMedia"] 