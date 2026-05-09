from fastapi import APIRouter
from app.modules.auth.schemas import DNIRegisterRequest, ImmigrationCardRegisterRequest, LoginRequest, TokenResponse
from app.modules.auth.service import login_with_dni, register_with_dni, register_with_immigrationcard

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