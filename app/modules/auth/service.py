from sqlalchemy.orm import Session

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


def login_with_dni(data : LoginRequest):
    ## COMPLETAR LOGICA
    return None



def register_with_dni(data: DNIRegisterRequest):

    db: Session = SessionLocal()

    try:

        # =========================
        # VALIDAR DUPLICADOS
        # =========================

        existing_email = db.query(User).filter(
            User.email == data.email
        ).first()

        if existing_email:
            raise Exception("El correo ya existe")

        existing_dni = db.query(User).filter(
            User.document_number == data.dni
        ).first()

        if existing_dni:
            raise Exception("El DNI ya existe")

        # =========================
        # VALIDAR RENIEC
        # =========================

        reniec = ReniecClient()

        reniec_data = reniec.validate_dni(
            data.dni
        )

        if not reniec_data:
            raise Exception("DNI no válido")

        # =========================
        # HASH PASSWORD
        # =========================

        hashed_password = hash_password(
            data.password
        )

        # =========================
        # CREAR USUARIO
        # =========================

        user = User(
            full_name=data.fullname,
            email=data.email,
            password=hashed_password,
            document_type="dni",
            document_number=data.dni,
            user_type=data.user_type
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        # =========================
        # TOKEN
        # =========================

        token = create_token({
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        db.close()


def register_with_immigrationcard(
        data: ImmigrationCardRegisterRequest
):

    db: Session = SessionLocal()

    try:

        # =========================
        # VALIDAR DUPLICADOS
        # =========================

        existing_email = db.query(User).filter(
            User.email == data.email
        ).first()

        if existing_email:
            raise Exception("El correo ya existe")

        existing_document = db.query(User).filter(
            User.document_number == data.immigration_card
        ).first()

        if existing_document:
            raise Exception(
                "El carnet ya existe"
            )

        # =========================
        # HASH PASSWORD
        # =========================

        hashed_password = hash_password(
            data.password
        )

        # =========================
        # CREAR USUARIO
        # =========================

        user = User(
            full_name=data.fullname,
            email=data.email,
            password=hashed_password,
            document_type="immigration_card",
            document_number=data.immigration_card,
            user_type= data.user_type
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        # =========================
        # TOKEN
        # =========================

        token = create_token({
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        db.close()