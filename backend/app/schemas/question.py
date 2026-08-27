from pydantic import BaseModel


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str
    topic: str | None = None
    difficulty: str | None = None
    marks: int
    options: str | None = None
    correct_answer: str | None = None


class QuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    topic: str | None
    difficulty: str | None
    marks: int
    options: str | None
    correct_answer: str | None
    is_active: bool