from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.assessment import Assessment
from app.models.assignment import ClassTeacherSubjectAssignment
from app.models.question import Question
from app.models.teacher import TeacherProfile
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
)


router = APIRouter(
    prefix="/teachers",
    tags=["Questions"],
)


@router.post(
    "/assessments/{assessment_id}/questions",
    response_model=QuestionResponse,
)
def create_question(
    assessment_id: int,
    request: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    teacher = (
        db.query(TeacherProfile)
        .filter(
            TeacherProfile.user_id == current_user.id
        )
        .first()
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher profile not found",
        )

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    if assessment.teacher_id != teacher.id:
        raise HTTPException(
            status_code=403,
            detail="You do not own this assessment",
        )

    if request.marks <= 0:
        raise HTTPException(
            status_code=400,
            detail="Question marks must be greater than 0",
        )

    question = Question(
        assessment_id=assessment.id,
        question_text=request.question_text,
        question_type=request.question_type,
        topic=request.topic,
        difficulty=request.difficulty,
        marks=request.marks,
        options=request.options,
        correct_answer=request.correct_answer,
        is_active=True,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get(
    "/assessments/{assessment_id}/questions",
    response_model=list[QuestionResponse],
)
def get_assessment_questions(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    teacher = (
        db.query(TeacherProfile)
        .filter(
            TeacherProfile.user_id == current_user.id
        )
        .first()
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher profile not found",
        )

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id,
            Assessment.teacher_id == teacher.id,
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return (
        db.query(Question)
        .filter(
            Question.assessment_id == assessment_id,
            Question.is_active == True,
        )
        .all()
    )