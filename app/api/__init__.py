from fastapi import APIRouter
from app.api.endpoints import products, vendors

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])