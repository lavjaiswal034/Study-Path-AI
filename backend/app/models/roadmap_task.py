from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    roadmap_id: Mapped[int] = mapped_column(
        ForeignKey("roadmaps.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    task_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="STUDY",
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="MEDIUM",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    estimated_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )