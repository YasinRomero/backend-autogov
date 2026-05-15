from fastapi import HTTPException
from sqlalchemy.orm import Session
import re
import unicodedata

from app.modules.auth.schemas import (
    DNIRegisterRequest,
    ImmigrationCardRegisterRequest,
    LoginRequest
)

from app.models.user import User

from app.db.session import SessionLocal

from app.integrations.reniec.client import ReniecClient

from app.core.security import (
    create_token,
    hash_password,
    verify_password_hash
)


# =========================================
# UTILIDADES
# =========================================

# Este funciona en los nombres del form y de RENIEC. Les da un formato para compararlos y ver si coinciden
def clean_text(text: str):

    return (
        unicodedata.normalize("NFD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .replace(",", "")
        .lower()
        .strip()
    )

def validate_password(password: str):

    # La contrasena debe tener minimo 8 caracteres
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener mínimo 8 caracteres"
        )
    # La contrasena debe tener al menos una mayuscula
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos una mayúscula"
        )

    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos un número"
        )

