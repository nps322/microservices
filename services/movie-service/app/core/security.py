import jwt

from app.core.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

def decode_jwt(token:str) -> dict | None:

    result = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return result