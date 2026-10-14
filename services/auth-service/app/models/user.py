import enum

from datetime import datetime


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, Enum as SAEnum, Boolean, DateTime


from app.db.base import Base



class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True,nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(
                Role,
                name="user_role",
                values_callable=lambda enum_cls: [role.value for role in enum_cls],
            ),
            nullable=False,
            default=Role.USER,)
    