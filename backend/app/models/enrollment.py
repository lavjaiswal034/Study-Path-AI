from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student_profiles.id"),
        nullable=False,
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey("classes.id"),
        nullable=False,
    )

    academic_year_id: Mapped[int] = mapped_column(
        ForeignKey("academic_years.id"),
        nullable=False,
    )

    enrollment_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )