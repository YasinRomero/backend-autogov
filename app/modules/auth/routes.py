from fastapi import APIRouter, Depends
from app.modules.auth.schemas import DNIRegisterRequest, ImmigrationCardRegisterRequest, LoginRequest, TokenResponse
from app.modules.auth.service import login_with_dni, register_with_dni, register_with_immigrationcard, logout_user
from app.modules.auth.dependencies import get_current_user
router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    return login_with_dni(data)

@router.post("/register/dni", response_model=TokenResponse)
def dniRegister(data: DNIRegisterRequest):
    return register_with_dni(data)

@router.post("/register/inmigrationcard", response_model=TokenResponse)
def inmiCardRegister(data: ImmigrationCardRegisterRequest):
    return register_with_immigrationcard(data)

@router.post("/logout")
def logout(current_user = Depends(get_current_user)):
    return logout_user()