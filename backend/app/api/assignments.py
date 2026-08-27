from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.assignment import (
    ClassTeacherSubjectAssignment,
)
from app.models.user import User
from app.schemas.assignment import (
    TeacherAssignmentCreate,
    TeacherAssignmentResponse,
)


router = APIRouter(
    prefix="/admin/assignments",
    tags=["Teacher Assignments"],
)


@router.post(
    "",
    response_model=TeacherAssignmentResponse,
)
def create_assignment(
    request: TeacherAssignmentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    existing = (
        db.query(ClassTeacherSubjectAssignment)
        .filter(
            ClassTeacherSubjectAssignment.teacher_id
            == request.teacher_id,
            ClassTeacherSubjectAssignment.class_id
            == request.class_id,
            ClassTeacherSubjectAssignment.subject_id
            == request.subject_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="This teacher is already assigned to this class and subject",
        )

    assignment = ClassTeacherSubjectAssignment(
        teacher_id=request.teacher_id,
        class_id=request.class_id,
        subject_id=request.subject_id,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


@router.get(
    "",
    response_model=list[TeacherAssignmentResponse],
)
def get_assignments(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return db.query(ClassTeacherSubjectAssignment).all()