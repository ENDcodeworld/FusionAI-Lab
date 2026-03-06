"""
API Router
"""

from fastapi import APIRouter
from app.api.routes import (
    companies,
    funding,
    papers,
    experiments,
    reports,
    users,
    auth
)

# Create main API router
api_router = APIRouter()

# Include route modules
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(funding.router, prefix="/funding", tags=["funding"])
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
