from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )