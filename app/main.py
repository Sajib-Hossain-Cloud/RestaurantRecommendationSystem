from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.core.config import settings
from app.api.v1.routes import api_router
from app.api.core.components.recommendation_service import recommendation_service


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered restaurant recommendation system with JWT authentication",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    
    print("Loading recommendation models...")
    recommendation_service.load_models()

@app.get("/")
async def root():
    
    return {
        "message": "Restaurant Recommendation API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
