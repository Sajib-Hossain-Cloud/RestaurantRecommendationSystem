from fastapi import APIRouter
from app.api.v1.endpoints import health, recommendation, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(recommendation.router, tags=["recommendations"])
