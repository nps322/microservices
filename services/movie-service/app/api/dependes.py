
from  jwt import PyJWTError
from aiokafka import AIOKafkaProducer
from fastapi import Depends, status, HTTPException , Request
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.director import DirectorRepository
from app.repositories.movie import MovieRepository
from app.services.movie import MovieService
from app.services.director import DirectorService
from app.db.session import get_db

from app.core.security import decode_jwt

from app.schemas.user import TokenUser

security = HTTPBearer()


async def get_kafka_producer(request: Request):
    return request.app.state.kafka_producer

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
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
    user_id = payload.get("sub")
    if not user_id:
        raise auth_exception    
    return TokenUser(user_id=user_id)

async def get_director_service(session: AsyncSession = Depends(get_db)):
    repository = DirectorRepository(session)
    return DirectorService(repository)

async def get_movie_service(
    session: AsyncSession = Depends(get_db),
    producer: AIOKafkaProducer = Depends(get_kafka_producer)
) -> MovieService:
    
    director = DirectorRepository(session)
    repository = MovieRepository(session)
    return MovieService(repository= repository,producer=producer,director_repository=director)
