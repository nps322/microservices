from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie
from app.models.genre import Genre

from app.schemas.pymodel import CreateMovie

from app.core.exception import MovieAlreadyExistsError

class MovieRepository():

    def __init__(self, session: AsyncSession,):
        self.session = session


    async def get_by_id(self, movie_id: int) -> Movie | None:

        stmt = select(Movie).where(Movie.id == movie_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_title(self, title:str) -> Movie | None:

        stmt = select(Movie).where(Movie.title == title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_genres(self, genres_id: list[int]):

        stmt = select(Genre).where((Genre.id).in_(genres_id))
        result = await self.session.execute(stmt)
        generes = result.scalars().all()
        return generes

    async def create_movie(self, data: CreateMovie) -> Movie:
        result = await self.get_by_title(data.title)
        if result is not None:
            raise MovieAlreadyExistsError(data.title)
        genres = await self.get_genres(data.genre_ids)
        new_movie = Movie(title= data.title,
                        director_id= data.director_id,
                        genres= genres)

        self.session.add(new_movie)
        await self.session.flush()
        
        return new_movie


    async def get_all_movie(self, director_id: int|None, 
                            limit: int = 10,
                            offset: int = 0) -> list[Movie]:

        stmt = select(Movie)
        if director_id is not None:
            stmt = stmt.where(Movie.director_id == director_id)

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)

        return result.scalars().all()

