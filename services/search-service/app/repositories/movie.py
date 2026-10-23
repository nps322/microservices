from elasticsearch import AsyncElasticsearch,NotFoundError
from app.elastic.indexes import INDEX_SETTINGS, MOVIE_MAPPING


from app.schemas.movie import MovieSearchDocument

from app.core.exception import DocumentNotFoundError

class MovieSearchRepository:

    def __init__(self, client: AsyncElasticsearch, index_name: str,):
        self.client = client
        self.index_name = index_name


    async def prepare_index(self) -> None:
        exists = await self.client.indices.exists(index=self.index_name)

        if exists:
            return
        await self.client.indices.create(index=self.index_name, 
                                         settings=INDEX_SETTINGS,
                                         mappings=MOVIE_MAPPING)


    async def save(self, document: MovieSearchDocument) -> None:
        await self.client.index(
            index=self.index_name,
            id=str(document.id),
            document=document.model_dump(),)


    async def get(self, movie_id: int) -> MovieSearchDocument:
        try:
            response = await self.client.get(
                index=self.index_name,
                id=str(movie_id),)
        except NotFoundError:
            raise DocumentNotFoundError
        return MovieSearchDocument.model_validate(response["_source"])



    async def search(self, query: str, 
                     limit: int = 3, 
                     offset: int = 0,
                     director_id: int | None = None) -> list[MovieSearchDocument]:

        must_case = [{"match": {"title": query}}]
        filter_case = []

        if director_id is not None:
            filter_case.append({"term": {"director_id": director_id}})

        search_query = {"bool":{"must":must_case,
                                "filter":filter_case}}

        response = await self.client.search(
            index=self.index_name,
            query=search_query,
            size=limit,
            from_=offset)

        return [MovieSearchDocument(**hit["_source"]) for hit in response["hits"]["hits"]]