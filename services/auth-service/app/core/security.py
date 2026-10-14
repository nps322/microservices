import jwt

from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



def generate_jwt_token(
    user_id: int,
    email: str,
    expires_in_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_in_minutes)

    payload = {
        "sub": str(user_id),  
        "email": email,
        "iat": (now),  
        "exp": (expire),  
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt(token:str) -> dict | None:

    result = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return result
    

def get_password_hash(password: str) -> str:

    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return password_hash.verify(plain_password,hashed_password)



