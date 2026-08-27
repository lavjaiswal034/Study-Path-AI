from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )