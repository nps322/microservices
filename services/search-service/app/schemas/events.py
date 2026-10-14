from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class MovieCreatedPayloadV1(BaseModel):
    id: int
    title: str
    director_id: int
    director_name: str


class MovieCreatedV1(BaseModel):
    event_id: UUID
    event_type: Literal["movie.created"]
    event_version: Literal[1]
    occurred_at: datetime
    payload: MovieCreatedPayloadV1