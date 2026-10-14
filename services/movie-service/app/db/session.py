from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


from app.core.config import settings


db_url = settings.database_url

engine = create_async_engine(db_url, echo= True)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:

        yield session