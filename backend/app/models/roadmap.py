from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student_profiles.id"),
        nullable=False,
    )

    prediction_id: Mapped[int | None] = mapped_column(
        ForeignKey("predictions.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )