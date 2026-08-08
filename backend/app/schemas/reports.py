from pydantic import BaseModel
from typing import Any, List


class ReportRequest(BaseModel):
    student_id: int


class ReportResponse(BaseModel):
    student_id: int
    student_name: str
    generated_at: str
    analytics: dict[str, Any]
    prediction: dict[str, Any]
    roadmap: List[dict[str, Any]]