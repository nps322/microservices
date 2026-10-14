
from sqlalchemy import Table, Column, ForeignKey

from app.db.base import Base


movie_genre_association = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)