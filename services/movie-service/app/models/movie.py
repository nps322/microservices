from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


from app.db.base import Base


class Movie(Base):

    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=False,index=True)

    director_id: Mapped[int | None] = mapped_column(ForeignKey("directors.id", ondelete="SET NULL"))

    director: Mapped[Optional["Director"]]= relationship("Director", back_populates="movies")
    genres: Mapped[list["Genre"]] = relationship(
        secondary="movie_genre", back_populates="movies"
    )