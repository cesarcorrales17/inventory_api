from fastapi import APIRouter
from app.api.v1 import api_v1

api_router = APIRouter()

# Include API v1 router
api_router.include_router(api_v1.api_router, prefix="/v1")