from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.assessment import Assessment
from app.models.enrollment import StudentEnrollment
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.student_assessment import StudentAssessmentResponse


router = APIRouter(
    prefix="/students",
    tags=["Student Assessments"],
)


@router.get(
    "/assessments",
    response_model=list[StudentAssessmentResponse],
)
def get_available_assessments(
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
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    enrollments = (
        db.query(StudentEnrollment)
        .filter(
            StudentEnrollment.student_id == student.id,
            StudentEnrollment.enrollment_status == "ACTIVE",
        )
        .all()
    )

    class_ids = [
        enrollment.class_id
        for enrollment in enrollments
    ]

    if not class_ids:
        return []

    return (
        db.query(Assessment)
        .filter(
            Assessment.class_id.in_(class_ids)
        )
        .all()
    )