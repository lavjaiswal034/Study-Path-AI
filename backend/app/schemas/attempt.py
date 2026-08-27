from datetime import datetime

from pydantic import BaseModel


class AttemptResponse(BaseModel):
    id: int
    assessment_id: int
    student_id: int
    started_at: datetime
    submitted_at: datetime | None
    score: int | None
    status: str