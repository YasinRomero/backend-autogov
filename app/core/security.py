from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "llaveprivadaparatoken123wa"
ALGORITM = "HS256"

## Usen este metodo para convertir un diccionario a un JWT
def create_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)