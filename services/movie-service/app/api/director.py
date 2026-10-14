from fastapi import APIRouter, Depends, status

from app.services.director import DirectorService

from app.schemas.director import CreateDirector,DirectorResponse
from app.schemas.user import TokenUser

from app.api.dependes import get_director_service,get_current_user

director_router = APIRouter(prefix="/directors", tags=["director"])


@director_router.post("/", status_code=status.HTTP_201_CREATED, response_model= DirectorResponse)
async def create_director(data: CreateDirector,
    service: DirectorService = Depends(get_director_service),
    user: TokenUser = Depends(get_current_user)):

    result = await service.create_director(data)
    return result


@director_router.get("/", response_model= list[DirectorResponse])
async def get_directors(service: DirectorService = Depends(get_director_service)):

    result = await service.get_all_directors()
    return result

@director_router.get("/{director_id}", response_model=DirectorResponse)
async def get_director_by_id(director_id: int,
                             service: DirectorService = Depends(get_director_service)):

    result = await service.get_director(director_id)
    return result
