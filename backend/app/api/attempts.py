from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.assessment import Assessment
from app.models.attempt import AssessmentAttempt
from app.models.enrollment import StudentEnrollment
from app.models.response import AssessmentResponse
from app.models.student import StudentProfile
from app.models.user import User

from app.schemas.attempt import AttemptResponse
from app.schemas.result import AssessmentResultResponse


router = APIRouter(
    prefix="/students",
    tags=["Assessment Attempts"],
)


# ============================================================
# START ASSESSMENT ATTEMPT
# ============================================================

@router.post(
    "/assessments/{assessment_id}/attempt",
    response_model=AttemptResponse,
)
def start_attempt(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only students can start an assessment
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

    # Find assessment
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    # Check student enrollment
    enrollment = (
        db.query(StudentEnrollment)
        .filter(
            StudentEnrollment.student_id == student.id,
            StudentEnrollment.class_id == assessment.class_id,
            StudentEnrollment.enrollment_status == "ACTIVE",
        )
        .first()
    )

    if not enrollment:
        raise HTTPException(
            status_code=403,
            detail="You are not enrolled in this assessment's class",
        )

    # Check if student already has an active attempt
    existing_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.assessment_id == assessment_id,
            AssessmentAttempt.student_id == student.id,
            AssessmentAttempt.status == "IN_PROGRESS",
        )
        .first()
    )

    if existing_attempt:
        return existing_attempt

    # Create new attempt
    attempt = AssessmentAttempt(
        assessment_id=assessment_id,
        student_id=student.id,
        started_at=datetime.utcnow(),
        submitted_at=None,
        score=None,
        status="IN_PROGRESS",
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


# ============================================================
# SUBMIT ASSESSMENT ATTEMPT
# ============================================================

@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=AssessmentResultResponse,
)
def submit_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only students can submit
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

    # Find the attempt
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

    # Make sure attempt is still active
    if attempt.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=400,
            detail="Assessment attempt is already submitted",
        )

    # Get all responses
    responses = (
        db.query(AssessmentResponse)
        .filter(
            AssessmentResponse.attempt_id == attempt.id
        )
        .all()
    )

    # Calculate total score
    score = sum(
        response.marks_obtained or 0
        for response in responses
    )

    # Submission time
    submitted_at = datetime.utcnow()

    # Update attempt
    attempt.score = score
    attempt.submitted_at = submitted_at
    attempt.status = "SUBMITTED"

    db.commit()
    db.refresh(attempt)

    # Return result
    return AssessmentResultResponse(
        attempt_id=attempt.id,
        assessment_id=attempt.assessment_id,
        score=score,
        max_score=assessment.max_score,
        status=attempt.status,
        submitted_at=submitted_at,
    )