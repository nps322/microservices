from pydantic import BaseModel, Field, ConfigDict


class MovieSearchDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str
    director_id: int
    director_name: str


class MovieSearchParams(BaseModel):

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=200,)
    limit: int = Field(3, ge=1, le=100)
    offset: int = Field(0, ge=0)
    director_id: int | None = Field(None, ge=1)