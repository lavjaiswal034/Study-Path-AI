from pydantic import BaseModel, Field
from typing import List, Optional


class RoadmapRequest(BaseModel):
    student_id: int

    predicted_score: Optional[float] = None

    risk_level: str = Field(
        default="unknown"
    )

    weak_topics: List[str] = []

    study_hours_per_day: float = Field(
        default=2.0,
        ge=0,
        le=24,
    )


class RoadmapItem(BaseModel):
    topic: str
    priority: str
    estimated_hours: float
    description: str
    resources: List[str] = []


class RoadmapResponse(BaseModel):
    student_id: int
    roadmap: List[RoadmapItem]
    message: str