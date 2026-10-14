from fastapi import APIRouter, Depends, status

from app.services.movie import MovieService 

from app.schemas.pymodel import MovieResponse,CreateMovie
from app.schemas.user import TokenUser

from app.api.dependes import get_movie_service, get_current_user, get_kafka_producer

movie_router = APIRouter(prefix="/movies", tags=["movie"])


@movie_router.get("/", response_model=list[MovieResponse])
async def get_movies(director_id: int | None = None,
                    service: MovieService = Depends(get_movie_service),
                    limit: int = 10, 
                    offset: int = 0):

    result = await service.get_all_movie(director_id,
                                         limit,
                                         offset)
    return result


@movie_router.post("/", status_code=status.HTTP_201_CREATED, response_model=MovieResponse)
async def create_movie(data: CreateMovie,
                       service: MovieService = Depends(get_movie_service),
                       user: TokenUser = Depends(get_current_user)):

    result = await service.create_movie(data)
    return result