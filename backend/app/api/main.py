from fastapi import APIRouter

from app.api.routes import calculate

api_router = APIRouter()
api_router.include_router(calculate.router, prefix="/calculate", tags=["calculate"])
