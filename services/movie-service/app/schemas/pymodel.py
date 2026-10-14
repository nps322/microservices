from typing import List
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4


from pydantic import BaseModel, Field, ConfigDict





class CreateMovie(BaseModel):

    title: str = Field(min_length=1,max_length=255)
    director_id: int = Field(ge=1)
    genre_ids: List[int] = []


class MovieResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    director_id: int

class MovieCreatedPayloadV1(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    director_id: int
    director_name: str


class MovieCreatedV1(BaseModel):

    event_id: UUID = Field(default_factory=uuid4)
    event_type: Literal["movie.created"] = "movie.created"
    event_version: Literal[1] = 1

    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    payload: MovieCreatedPayloadV1