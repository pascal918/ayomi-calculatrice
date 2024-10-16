from fastapi import APIRouter

from app.api.routes import items, calculate, login, users,utils

api_router = APIRouter()
api_router.include_router(calculate.router, prefix="/calculate", tags=["calculate"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])

