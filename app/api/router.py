from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth_router,prefix="/auth",tags=["Auth"])