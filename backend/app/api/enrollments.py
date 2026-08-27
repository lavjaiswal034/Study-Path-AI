from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.student import StudentProfile
from app.models.enrollment import StudentEnrollment
from app.models.user import User
from app.schemas.enrollment import (
    StudentEnrollmentCreate,
    StudentEnrollmentResponse,
)


router = APIRouter(
    prefix="/students",
    tags=["Student Enrollment"],
)


@router.post(
    "/enrollment",
    response_model=StudentEnrollmentResponse,
)
def create_enrollment(
    request: StudentEnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )

    student = (
        db.query(StudentProfile)
        .filter(StudentProfile.user_id == current_user.id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    existing = (
        db.query(StudentEnrollment)
        .filter(
            StudentEnrollment.student_id == student.id,
            StudentEnrollment.academic_year_id
            == request.academic_year_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled for this academic year",
        )

    enrollment = StudentEnrollment(
        student_id=student.id,
        class_id=request.class_id,
        academic_year_id=request.academic_year_id,
        enrollment_status="ACTIVE",
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment