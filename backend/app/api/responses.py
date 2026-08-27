from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.attempt import AssessmentAttempt
from app.models.question import Question
from app.models.response import AssessmentResponse
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.response import (
    AssessmentResponseCreate,
    AssessmentResponseResponse,
)


router = APIRouter(
    prefix="/students",
    tags=["Assessment Responses"],
)


@router.post(
    "/attempts/{attempt_id}/responses",
    response_model=AssessmentResponseResponse,
)
def submit_response(
    attempt_id: int,
    request: AssessmentResponseCreate,
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

    if attempt.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=400,
            detail="This assessment attempt is no longer active",
        )

    question = (
        db.query(Question)
        .filter(
            Question.id == request.question_id,
            Question.assessment_id == attempt.assessment_id,
            Question.is_active == True,
        )
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found in this assessment",
        )

    existing_response = (
        db.query(AssessmentResponse)
        .filter(
            AssessmentResponse.attempt_id == attempt_id,
            AssessmentResponse.question_id == request.question_id,
        )
        .first()
    )

    if existing_response:
        raise HTTPException(
            status_code=400,
            detail="Response already submitted for this question",
        )

    is_correct = None
    marks_obtained = 0

    if request.answer is not None:
        is_correct = (
            request.answer.strip().lower()
            == question.correct_answer.strip().lower()
        )

        if is_correct:
            marks_obtained = question.marks

    response = AssessmentResponse(
        attempt_id=attempt_id,
        question_id=question.id,
        answer=request.answer,
        is_correct=is_correct,
        marks_obtained=marks_obtained,
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return response