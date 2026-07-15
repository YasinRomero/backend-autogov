from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.auth.schemas import (
    DNIRegisterRequest,
    ImmigrationCardRegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    UpdateEmailRequest
)
from app.modules.auth.service import (
    login_with_dni,
    register_with_dni,
    register_with_immigrationcard,
    logout_user,
    get_user_profile,
    update_user_email
)
from app.modules.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    """
    Inicia sesión de usuario utilizando su número de DNI o documento y contraseña.
    Retorna un token de acceso JWT si las credenciales son válidas.
    """
    return login_with_dni(data)

@router.post("/register/dni", response_model=TokenResponse)
def dniRegister(data: DNIRegisterRequest):
    """
    Registra un nuevo usuario en el sistema utilizando su número de DNI.
    Realiza la validación de identidad y retorna un token de acceso JWT.
    """
    return register_with_dni(data)

@router.post("/register/inmigrationcard", response_model=TokenResponse)
def inmiCardRegister(data: ImmigrationCardRegisterRequest):
    """
    Registra un nuevo usuario extranjero utilizando su Carné de Extranjería.
    Retorna un token de acceso JWT tras un registro exitoso.
    """
    return register_with_immigrationcard(data)

@router.post("/logout")
def logout(current_user = Depends(get_current_user)):
    """
    Cierra la sesión del usuario actual e invalida su token/sesión activa.
    """
    return logout_user()

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtiene la información de perfil del usuario actualmente autenticado.
    """
    return get_user_profile(user_id=current_user["user_id"], db=db)

@router.put("/me", response_model=UserResponse)
def update_me(data: UpdateEmailRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Actualiza el correo electrónico del usuario actualmente autenticado.
    """
    return update_user_email(user_id=current_user["user_id"], new_email=data.email, db=db)