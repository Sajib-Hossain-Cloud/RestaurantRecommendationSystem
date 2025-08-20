from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Recommendation API"
    VERSION: str = "1.0.0"
    
    
    SECRET_KEY: str = "Please write your own secret key as per technonext policy or generate one by endpoint"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:8000"]
    
    
    MODEL_PATH: str = "app/ai_service/notebooks/models/restaurant_recommender.pkl"
    DATA_PATH: str = "app/ai_service/notebooks/models/restaurant_data.csv"
    SIMILARITY_MATRIX_PATH: str = "app/ai_service/notebooks/models/similarity_matrix.npy"
    
    class Config:
       
        env_file = None
        case_sensitive = False
        extra = "ignore"

settings = Settings()
