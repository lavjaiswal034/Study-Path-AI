from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/teachers/pending")
def get_pending_teachers(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    teachers = (
        db.query(User)
        .filter(
            User.role == "teacher",
            User.approval_status == "pending",
        )
        .all()
    )

    return [
        {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "role": teacher.role,
            "approval_status": teacher.approval_status,
        }
        for teacher in teachers
    ]


@router.post("/teachers/{teacher_id}/approve")
def approve_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    teacher = (
        db.query(User)
        .filter(
            User.id == teacher_id,
            User.role == "teacher",
        )
        .first()
    )

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    if teacher.approval_status == "approved":
        return {
            "message": "Teacher is already approved",
            "teacher_id": teacher.id,
            "approval_status": teacher.approval_status,
        }

    if teacher.approval_status == "rejected":
        raise HTTPException(
            status_code=400,
            detail="Teacher application was rejected",
        )

    teacher.approval_status = "approved"

    db.commit()
    db.refresh(teacher)

    return {
        "message": "Teacher approved successfully",
        "teacher_id": teacher.id,
        "approval_status": teacher.approval_status,
    }