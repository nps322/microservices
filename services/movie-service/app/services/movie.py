from aiokafka import AIOKafkaProducer
from app.repositories.movie import MovieRepository
from app.schemas.pymodel import MovieResponse, MovieCreatedPayloadV1,MovieCreatedV1
from app.models.movie import Movie
from app.repositories.director import DirectorRepository
from app.schemas.pymodel import CreateMovie

from app.core.exception import DirectorNotFoundError



class MovieService():

    def __init__(self, repository:MovieRepository, 
                 producer: AIOKafkaProducer,
                 director_repository: DirectorRepository):

        self.repository = repository
        self.producer = producer
        self.director_repository = director_repository

    async def get_all_movie(self, director_id: int|None, 
                            limit: int = 10,
                            offset: int = 0) -> list[Movie]:

        result = await self.repository.get_all_movie(director_id,limit,offset)
        return result

    async def create_movie(self, data: CreateMovie):

        director = await self.director_repository.get_director_by_id(data.director_id)
        if director is None:
            raise DirectorNotFoundError
        movie_db = await self.repository.create_movie(data)
        await self.repository.session.commit()

        # нужно будет сделать транзакцию для commit и kafka event

        movie_payload = MovieCreatedPayloadV1(
            id=movie_db.id,
            title=movie_db.title,
            director_id=movie_db.director_id,
            director_name=director.name)
        movie_created = MovieCreatedV1(payload=movie_payload)
        movie_bytes = movie_created.model_dump_json().encode("utf-8")

        await self.producer.send_and_wait(
            topic="movie.created",
            value=movie_bytes,
            key=str(movie_created.payload.id).encode("utf-8"),
        )

        return movie_db

