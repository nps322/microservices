

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Table, Column, ForeignKey

from app.db.base import Base




class Genre(Base):

    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String,unique=True, nullable=False)

    movies: Mapped[list["Movie"]] = relationship(
        secondary="movie_genre", back_populates="genres"
    )



