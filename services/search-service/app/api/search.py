from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependens import get_movie_repository
from app.repositories.movie import MovieSearchRepository
from app.schemas.movie import MovieSearchDocument, MovieSearchParams

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/movie/", response_model= list[MovieSearchDocument])
async def get_movie_by_query(params: Annotated[MovieSearchParams, Depends()],
                             repository: MovieSearchRepository = Depends(get_movie_repository)):

    return await repository.search(query=params.query, 
                                   limit=params.limit, 
                                   offset=params.offset,
                                   director_id=params.director_id)

@router.get("/{id}/", response_model= MovieSearchDocument)
async def get_movies(id: int,
    repository: MovieSearchRepository = Depends(get_movie_repository)):

    return await repository.get(id)


