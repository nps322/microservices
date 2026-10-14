from pydantic import BaseModel,Field,ConfigDict

class CreateDirector(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1,max_length=55)

class DirectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    id: int