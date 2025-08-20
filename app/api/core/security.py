from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class UserManager:
    def __init__(self):
        self.users = {
            "admin": {
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Administrator",
                "hashed_password": pwd_context.hash("admin123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            "user": {
                "username": "user",
                "email": "user@example.com",
                "full_name": "Regular User",
                "hashed_password": pwd_context.hash("user123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            "test": {
                "username": "test",
                "email": "test@example.com",
                "full_name": "Test User",
                "hashed_password": pwd_context.hash("test123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        }
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        return self.users.get(username)
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return user

user_manager = UserManager()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_manager.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
