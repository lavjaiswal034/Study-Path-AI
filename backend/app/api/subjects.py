from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.subject import Subject
from app.models.user import User
from app.schemas.subject import (
    SubjectCreate,
    SubjectResponse,
)


router = APIRouter(
    prefix="/admin/subjects",
    tags=["Subjects"],
)


@router.post(
    "",
    response_model=SubjectResponse,
)
def create_subject(
    request: SubjectCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    existing_subject = (
        db.query(Subject)
        .filter(
            (Subject.code == request.code)
            | (Subject.name == request.name)
        )
        .first()
    )

    if existing_subject:
        raise HTTPException(
            status_code=400,
            detail="Subject with this name or code already exists",
        )

    subject = Subject(
        name=request.name,
        code=request.code,
        credits=request.credits,
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    return subject


@router.get(
    "",
    response_model=list[SubjectResponse],
)
def get_subjects(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return db.query(Subject).all()