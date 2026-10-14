from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.pymodels import UserCreate

from app.models.user import User

class UserRepositories():


    def __init__(self, session:AsyncSession):

        self.session = session

    async def get_by_email(self, user_email:str) -> User|None:

        stmt = select(User).where(User.email == user_email)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
        

    async def create_user(self, user:User) -> User:

        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user
        
        