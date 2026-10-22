from pydantic import BaseModel, ConfigDict


class MovieSearchDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    title: str
    director_id: int
    director_name: str
