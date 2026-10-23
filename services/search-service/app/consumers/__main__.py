import asyncio
import logging

from aiokafka import AIOKafkaConsumer

from app.core.config import settings, client
from app.schemas.events import MovieCreatedV1
from app.schemas.movie import MovieSearchDocument

from app.repositories.movie import MovieSearchRepository


logger = logging.getLogger(__name__)

async def run_worker() -> None:
    consumer = AIOKafkaConsumer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        enable_auto_commit=False,
        auto_offset_reset="earliest")

    consumer.subscribe(["movie.created"])

    async with client:
        repository = MovieSearchRepository(
            client=client,
            index_name=settings.index)

        await repository.prepare_index()
        logger.info("Индекс подготовлен: %s", settings.index)

        async with consumer:
            async for msg in consumer:
                event = MovieCreatedV1.model_validate_json(msg.value)

                doc = MovieSearchDocument(
                    id=event.payload.id,
                    title=event.payload.title,
                    director_id=event.payload.director_id,
                    director_name=event.payload.director_name)
                await repository.save(doc)
                
                logger.info(
                    "Document created: movie_id=%s title=%s",
                    doc.id,
                    doc.title)
                
                await consumer.commit()
logging.basicConfig(level=logging.INFO)
asyncio.run(run_worker())