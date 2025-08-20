from fastapi import APIRouter, Depends
from datetime import datetime
from app.api.core.config import settings
from app.api.core.components.recommendation_service import recommendation_service
from app.api.core.security import get_current_user

router = APIRouter()

@router.get("/health")
async def health_check(current_user: dict = Depends(get_current_user)):
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.VERSION,
        "model_loaded": recommendation_service.is_loaded,
        "user": {
            "username": current_user["username"],
            "email": current_user["email"]
        }
    }

@router.get("/health/public")
async def public_health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.VERSION,
        "model_loaded": recommendation_service.is_loaded
    }
