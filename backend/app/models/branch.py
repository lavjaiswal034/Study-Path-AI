from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )