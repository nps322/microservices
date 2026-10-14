from fastapi import Request

from app.core.config import client, settings
from app.repositories.movie import MovieSearchRepository


async def get_movie_repository(request:Request) -> MovieSearchRepository:

    return request.app.state.movie_repository