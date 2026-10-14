from app.repositories.movie import MovieSearchRepository
from app.core.config import client
import asyncio

async def main():
    repository = MovieSearchRepository(client=client, index_name="movies")
    document = await repository.get(7)
    print(document.title)


if __name__ == "__main__":
    asyncio.run(main())