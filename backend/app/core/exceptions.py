"""
Custom exception handlers for the application.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle SQLAlchemy IntegrityError exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": "Database constraint violation"}
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    ) 