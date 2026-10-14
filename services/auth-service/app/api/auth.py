from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 


from app.schemas.pymodels import (UserCreate,
                                  UserResponse,
                                  UserLogin,
                                  Token)

from app.services.user import UserService

from app.api.dependencies import get_user_service



router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    user = await service.register_user(user_data)
    return user


@router.post("/login", response_model=Token)
async def login_user(user_data:UserLogin,
                     service: UserService = Depends(get_user_service)):
    jwt = await service.login_user(user_data.email, user_data.password)

    return Token(access_token=jwt)


