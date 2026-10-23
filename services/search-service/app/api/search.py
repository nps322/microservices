from fastapi import APIRouter, Depends
from app.api.dependens import get_movie_repository
from app.repositories.movie import MovieSearchRepository
from app.schemas.movie import MovieSearchDocument

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/movie/", response_model= list[MovieSearchDocument])
async def get_movie_by_query(query: str,
                             limit: int = 3,
                             offset:int = 0,
                             director_id: int | None = None,
                             repository: MovieSearchRepository = Depends(get_movie_repository)):

    return await repository.search(query, 
                                   limit=limit, 
                                   offset=offset,
                                   director_id=director_id)

@router.get("/{id}/")
async def get_movies(id: int,
    repository: MovieSearchRepository = Depends(get_movie_repository)):

    return await repository.get(id)


