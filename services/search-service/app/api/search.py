from fastapi import APIRouter, Depends
from app.api.dependens import get_movie_repository
from app.repositories.movie import MovieSearchRepository

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/{id}/")
async def get_movies(id: int,
    repository: MovieSearchRepository = Depends(get_movie_repository)):

    return await repository.get(id)