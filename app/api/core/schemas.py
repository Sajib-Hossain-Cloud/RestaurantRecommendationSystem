from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime


class RestaurantBase(BaseModel):
    name: str
    location: str
    cuisines: str
    cost_clean: float
    rating_clean: float
    rest_type: str

class RestaurantResponse(RestaurantBase):
    id: int
    similarity_score: Optional[float] = None


class RecommendationRequest(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant to get recommendations for")
    top_n: int = Field(default=10, ge=1, le=50, description="Number of recommendations")
    min_similarity: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum similarity threshold")

class RecommendationResponse(BaseModel):
    query_restaurant: RestaurantResponse
    recommendations: List[RestaurantResponse]
    total_recommendations: int
    avg_similarity: float
    diversity_score: float
    coverage_score: float


class ColdStartRequest(BaseModel):
    name: str = Field(..., description="Restaurant name")
    cuisines: str = Field(..., description="Cuisine types (comma-separated)")
    location: str = Field(..., description="Location")
    cost_clean: float = Field(..., ge=0, description="Cost for two people")
    rating_clean: float = Field(..., ge=0, le=5, description="Rating (0-5)")
    rest_type: str = Field(..., description="Restaurant type")

class ColdStartResponse(BaseModel):
    new_restaurant: ColdStartRequest
    recommendations: List[RestaurantResponse]
    avg_similarity: float
    diversity_score: float


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    location: Optional[str] = None
    cuisine: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_cost: Optional[float] = Field(None, ge=0)
    limit: int = Field(default=20, ge=1, le=100)

class SearchResponse(BaseModel):
    query: str
    results: List[RestaurantResponse]
    total_results: int
    search_time_ms: float


class AnalyticsResponse(BaseModel):
    total_restaurants: int
    total_cuisines: int
    total_locations: int
    avg_rating: float
    avg_cost: float
    model_performance: Dict[str, Any]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    model_loaded: bool
