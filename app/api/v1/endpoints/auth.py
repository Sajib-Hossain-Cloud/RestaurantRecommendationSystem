from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from app.api.core.security import create_access_token, user_manager, get_current_user
from app.api.core.config import settings
from datetime import datetime

router = APIRouter()

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = user_manager.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": user["username"],
        "username": user["username"],
        "email": user["email"]
    }
    access_token = create_access_token(data=token_data)
    
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


@router.get("/test-users")
async def get_test_users():
    return {
        "message": "Test users for development",
        "users": [
            {"username": "admin", "password": "admin123"},
            {"username": "user", "password": "user123"},
            {"username": "test", "password": "test123"}
        ],
        "note": "Remove this endpoint in production"
    }
