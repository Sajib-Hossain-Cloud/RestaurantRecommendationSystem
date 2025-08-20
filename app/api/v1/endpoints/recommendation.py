from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from app.api.core.components.recommendation_service import recommendation_service
from app.api.core.security import get_current_user

router = APIRouter()


class RecommendationRequest(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant to get recommendations for")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of recommendations")
    min_similarity: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity threshold")

class RecommendationResponse(BaseModel):
    query_restaurant: dict
    recommendations: list
    total_recommendations: int
    avg_similarity: float
    diversity_score: float
    coverage_score: float

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user)
):
    
    
    if not recommendation_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation service is not ready. Models not loaded."
        )
    
    
    result = recommendation_service.get_recommendations(
        restaurant_name=request.restaurant_name,
        top_n=request.top_n,
        min_similarity=request.min_similarity
    )
    
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["error"]
        )
    
    return result

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_user)):
    
    
    analytics = recommendation_service.get_analytics()
    
    if "error" in analytics:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=analytics["error"]
        )
    
    return analytics
