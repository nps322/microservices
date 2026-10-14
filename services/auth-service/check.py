import asyncio

from sqlalchemy import text

from app.db.session import engine


async def check_db():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT current_database()"))
        return (result.scalar())
    
if __name__ == "__main__":
    asyncio.run(check_db())