"""
Main API router with all endpoints.
"""

from fastapi import APIRouter

from app.api.endpoints import analytics, predictions, auth, instagram

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"]) 