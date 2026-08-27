from datetime import datetime

from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    title: str
    description: str | None = None
    class_id: int
    subject_id: int
    assessment_type: str = "QUIZ"
    max_score: int


class AssessmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    class_id: int
    subject_id: int
    teacher_id: int
    assessment_type: str
    max_score: int
    created_at: datetime