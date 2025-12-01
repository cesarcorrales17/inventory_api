from fastapi import APIRouter
from app.api.v1.routers import inventory, users

api_router = APIRouter()

api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
