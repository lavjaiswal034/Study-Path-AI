from datetime import datetime

from pydantic import BaseModel


class AssessmentResultResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    score: int
    max_score: int
    status: str
    submitted_at: datetime