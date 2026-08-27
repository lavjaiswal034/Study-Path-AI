from pydantic import BaseModel


class AssessmentResponseCreate(BaseModel):
    question_id: int
    answer: str | None = None


class AssessmentResponseResponse(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    answer: str | None
    is_correct: bool | None
    marks_obtained: int | None