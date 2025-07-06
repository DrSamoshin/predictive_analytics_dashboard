"""
Main FastAPI application entry point for Instagram Predictive Analytics Dashboard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.api.routes import api_router
from app.core.exceptions import integrity_error_handler, general_exception_handler
# Import models to register them with SQLAlchemy
from app.models import User, InstagramAccount, InstagramMedia  # noqa: F401

app = FastAPI(
    title="Instagram Predictive Analytics Dashboard API",
    description="Backend API for Instagram analytics and predictions",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "Instagram Predictive Analytics Dashboard API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 