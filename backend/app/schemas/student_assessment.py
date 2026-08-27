from pydantic import BaseModel


class StudentAssessmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    class_id: int
    subject_id: int
    assessment_type: str
    max_score: int