from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.assessment import Assessment
from app.models.assignment import ClassTeacherSubjectAssignment
from app.models.teacher import TeacherProfile
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
)


router = APIRouter(
    prefix="/teachers",
    tags=["Assessments"],
)


@router.post(
    "/assessments",
    response_model=AssessmentResponse,
)
def create_assessment(
    request: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only teachers can create assessments
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    # Find teacher profile
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

    # Check whether this teacher is assigned
    # to the requested class + subject
    assignment = (
        db.query(ClassTeacherSubjectAssignment)
        .filter(
            ClassTeacherSubjectAssignment.teacher_id
            == teacher.id,
            ClassTeacherSubjectAssignment.class_id
            == request.class_id,
            ClassTeacherSubjectAssignment.subject_id
            == request.subject_id,
        )
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this class and subject",
        )

    if request.max_score <= 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum score must be greater than 0",
        )

    assessment = Assessment(
        title=request.title,
        description=request.description,
        class_id=request.class_id,
        subject_id=request.subject_id,
        teacher_id=teacher.id,
        assessment_type=request.assessment_type,
        max_score=request.max_score,
        created_at=datetime.utcnow(),
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment