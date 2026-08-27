from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.assessment import Assessment
from app.models.attempt import AssessmentAttempt
from app.models.student import StudentProfile
from app.models.user import User

from app.schemas.result import AssessmentResultResponse


router = APIRouter(
    prefix="/students",
    tags=["Assessment Results"],
)


@router.get(
    "/attempts/{attempt_id}/result",
    response_model=AssessmentResultResponse,
)
def get_attempt_result(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only students can view their results
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )

    # Find student profile
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

    # Find the student's attempt
    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.student_id == student.id,
        )
        .first()
    )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Assessment attempt not found",
        )

    # Student cannot view an unfinished result
    if attempt.status != "SUBMITTED":
        raise HTTPException(
            status_code=400,
            detail="Assessment has not been submitted yet",
        )

    # Find assessment
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == attempt.assessment_id
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return AssessmentResultResponse(
        attempt_id=attempt.id,
        assessment_id=attempt.assessment_id,
        score=attempt.score or 0,
        max_score=assessment.max_score,
        status=attempt.status,
        submitted_at=attempt.submitted_at,
    )