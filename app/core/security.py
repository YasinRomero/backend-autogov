from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "llaveprivadaparatoken123wa"
ALGORITM = "HS256"

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