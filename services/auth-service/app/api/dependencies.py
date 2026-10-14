from jwt import PyJWTError

from fastapi import Depends,HTTPException,status

from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession


from app.services.user import UserService

from app.db.session import get_async_session

from app.repositories.user import UserRepositories

from app.core.security import decode_jwt

security = HTTPBearer()


async def get_user_service(
    session: AsyncSession = Depends(get_async_session)
) -> UserService:

    repository = UserRepositories(session)
    return UserService(repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UserService = Depends(get_user_service)
):

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь не авторизован",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    
    token = credentials.credentials

    try:
        payload = decode_jwt(token)
    except PyJWTError:
        raise auth_exception
        
    email = payload.get("email")
    if not email:
        raise auth_exception
        
    user = await service.get_user_by_email(email)
    if not user:
        raise auth_exception

    return user