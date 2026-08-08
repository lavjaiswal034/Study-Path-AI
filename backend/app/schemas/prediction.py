from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    attendance: float = Field(
        ge=0,
        le=100,
        description="Student attendance percentage",
    )

    assignment_score: float = Field(
        ge=0,
        le=100,
        description="Assignment score",
    )

    previous_score: float = Field(
        ge=0,
        le=100,
        description="Previous academic score",
    )

    study_hours: float = Field(
        ge=0,
        le=24,
        description="Average study hours per day",
    )


class PredictionResult(BaseModel):
    predicted_score: Optional[float] = None
    risk_level: str
    confidence: Optional[float] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: str


class PredictionResponse(BaseModel):
    student_id: int
    prediction: PredictionResult
    notification: NotificationResponse