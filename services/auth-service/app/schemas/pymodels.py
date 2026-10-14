
from pydantic import BaseModel, ConfigDict, Field, EmailStr



class UserCreate(BaseModel):
    user_name: str = Field(min_length=4, max_length=12)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserResponse(BaseModel):
    id:int
    user_name: str = Field(min_length=4, max_length=12)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"
