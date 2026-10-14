from app.repositories.director import DirectorRepository
from app.models.directors import Director

from app.schemas.director import CreateDirector


class DirectorService():

    def __init__(self, repository:DirectorRepository):

        self.repository = repository



    async def create_director(self, data:CreateDirector):
        
        res =  await self.repository.create_director(data)
        await self.repository.session.commit()
        return res

    async def get_director(self, id:int):
        return await self.repository.get_director_by_id(id)

    async def get_all_directors(self):
        return await self.repository.get_directors()