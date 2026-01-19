from fastapi import APIRouter
from app.api.v1.routes import health, coverage, export

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(coverage.router, tags=["coverage"])
api_router.include_router(export.router, tags=["export"])
