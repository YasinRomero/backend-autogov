from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

SECRET_KEY = "llaveprivadaparatoken123wa"
ALGORITM = "HS256"
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

## Usen este metodo para convertir un diccionario a un JWT
def create_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)



## Usen este metodo para validar tokens
def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITM])
        
        return payload

    except JWTError:
        return None

## Este metodo hashea la contrasena con bycript
def hash_password(password: str):
    return pwd_context.hash(password)

## Este metodo compara la contrasena ingresada por el usuario con la almacenada en la bd que esta hasheada
def verify_password_hash(password: str, hashed: str):
    return pwd_context.verify(password, hashed)