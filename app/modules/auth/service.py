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


