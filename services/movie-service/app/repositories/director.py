from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.directors import Director


from app.schemas.director import CreateDirector

from app.core.exception import DirectorNotFoundError
class DirectorRepository():

    def __init__(self,session:AsyncSession):
        self.session = session


    async def create_director(self, data:CreateDirector):

        new_director = Director(name=data.name)
        self.session.add(new_director)
        await self.session.flush()
        return new_director


    async def get_director_by_id(self,id:int) -> Director | None: 

        smtm = select(Director).where(Director.id == id)
        result = await self.session.execute(smtm)
        director = result.scalar_one_or_none()
        return director
    
    async def get_directors(self):

        smtm = select(Director)
        result = await self.session.execute(smtm)
        return result.scalars().all()
