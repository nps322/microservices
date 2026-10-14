from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiokafka import AIOKafkaProducer

from app.core.exception import DirectorNotFoundError, MovieAlreadyExistsError

from app.core.config import settings
from app.api.director import director_router
from app.api.movie import movie_router


bootstrap = settings.kafka_bootstrap_servers
@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = AIOKafkaProducer(bootstrap_servers=bootstrap)
    await producer.start()

    app.state.kafka_producer = producer 
    yield
    
    await producer.stop()

app = FastAPI(lifespan=lifespan)


app.include_router(movie_router)
app.include_router(director_router)


@app.exception_handler(MovieAlreadyExistsError)
async def user_exists_handler(request: Request, 
                                     exc: MovieAlreadyExistsError):
    
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(DirectorNotFoundError)
async def director_not_found(request: Request, 
                                     exc: DirectorNotFoundError):
    
    return JSONResponse(status_code=404, content={"detail": str(exc)})