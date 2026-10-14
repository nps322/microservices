from contextlib import asynccontextmanager

from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse


from app.core.config import client, settings
from app.repositories.movie import MovieSearchRepository
from app.api.search import router
from app.core.exception import DocumentNotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = MovieSearchRepository(
        client=client,
        index_name=settings.index,
    )
    try:
        await repository.prepare_index()
        app.state.movie_repository = repository
        yield
    finally:
        await client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.exception_handler(DocumentNotFoundError)
async def user_exists_handler(request: Request, 
                                     exc: DocumentNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})