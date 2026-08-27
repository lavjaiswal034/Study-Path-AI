from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    teacher_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    employee_id: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="teacher_profile",
    )