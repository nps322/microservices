import asyncio
import logging

from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.events import MovieCreatedV1


logger = logging.getLogger(__name__)


async def run_worker() -> None:
    consumer = AIOKafkaConsumer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )

    consumer.subscribe(["movie.created"])

    try:
        await consumer.start()

        async for msg in consumer:
            try:
                event = MovieCreatedV1.model_validate_json(
                    msg.value
                )
            except ValidationError:
                logger.exception(
                    "Invalid event: partition=%s offset=%s",
                    msg.partition,
                    msg.offset,
                )
                raise

            logger.info(
                "event_id=%s movie_id=%s partition=%s offset=%s",
                event.event_id,
                event.payload.id,
                msg.partition,
                msg.offset,
            )

    finally:
        await consumer.stop()


logging.basicConfig(level=logging.INFO)
asyncio.run(run_worker())