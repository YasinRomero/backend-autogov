from fastapi import APIRouter
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import login_with_dni

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    return login_with_dni(data.dni)