from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
    String(100),
    nullable=False,
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    student_profile = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
    )

    teacher_profile = relationship(
        "TeacherProfile",
        back_populates="user",
        uselist=False,
    )
    approval_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime,
    nullable=False,
    default=datetime.utcnow,
)