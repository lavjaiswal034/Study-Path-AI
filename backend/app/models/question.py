from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    topic: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    difficulty: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    marks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    options: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    correct_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )