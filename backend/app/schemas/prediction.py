from datetime import datetime

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    F001_ATTENDANCE_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F002_ASSESSMENT_AVG_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F003_ASSIGNMENT_AVG_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F004_ASSIGNMENT_COMPLETION_RATE: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F005_QUIZ_AVG_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F006_QUIZ_COMPLETION_RATE: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F007_LAB_AVG_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F008_INTERNAL_ASSESSMENT_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F009_PREVIOUS_SEM_PCT: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    F011_BACKLOG_COUNT: float | None = Field(
        default=None,
        ge=0,
    )

    F017_ASSESSMENT_PARTICIPATION_RATE: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    final_exam_max_marks: float | None = Field(
        default=None,
        gt=0,
    )


class PredictionResponse(BaseModel):
    id: int
    prediction_type: str
    prediction_value: str

    risk_level: str | None
    confidence: float | None

    model_version: str | None
    created_at: datetime