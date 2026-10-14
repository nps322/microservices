
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import List


from app.db.base import Base


class Director(Base):

    __tablename__ = "directors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    movies: Mapped[List["Movie"]] = relationship("Movie", back_populates="director")