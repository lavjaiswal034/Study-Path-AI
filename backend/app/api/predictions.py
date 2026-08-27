from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.prediction import Prediction
from app.models.student import StudentProfile
from app.models.user import User

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)

from app.services.prediction_service import (
    predict_student_performance,
)


router = APIRouter(
    prefix="/students",
    tags=["Predictions"],
)


@router.post(
    "/predictions",
    response_model=PredictionResponse,
)
async def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )

    student = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    features = {
        "F001_ATTENDANCE_PCT": request.F001_ATTENDANCE_PCT,
        "F002_ASSESSMENT_AVG_PCT": request.F002_ASSESSMENT_AVG_PCT,
        "F003_ASSIGNMENT_AVG_PCT": request.F003_ASSIGNMENT_AVG_PCT,
        "F004_ASSIGNMENT_COMPLETION_RATE": request.F004_ASSIGNMENT_COMPLETION_RATE,
        "F005_QUIZ_AVG_PCT": request.F005_QUIZ_AVG_PCT,
        "F006_QUIZ_COMPLETION_RATE": request.F006_QUIZ_COMPLETION_RATE,
        "F007_LAB_AVG_PCT": request.F007_LAB_AVG_PCT,
        "F008_INTERNAL_ASSESSMENT_PCT": request.F008_INTERNAL_ASSESSMENT_PCT,
        "F009_PREVIOUS_SEM_PCT": request.F009_PREVIOUS_SEM_PCT,
        "F011_BACKLOG_COUNT": request.F011_BACKLOG_COUNT,
        "F017_ASSESSMENT_PARTICIPATION_RATE": request.F017_ASSESSMENT_PARTICIPATION_RATE,
    }

    result = await predict_student_performance(
        features=features,
        final_exam_max_marks=request.final_exam_max_marks,
    )

    prediction = Prediction(
        student_id=student.id,
        prediction_type="STUDENT_PERFORMANCE",
        prediction_value=str(
            result["predicted_percentage"]
        ),
        risk_level=result.get("risk_level"),
        confidence=result.get(
            "confidence_or_uncertainty"
        ),
        model_version=result.get("model_version"),
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


@router.get(
    "/predictions",
    response_model=list[PredictionResponse],
)
def get_prediction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )

    student = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.user_id == current_user.id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found",
        )

    predictions = (
        db.query(Prediction)
        .filter(
            Prediction.student_id == student.id
        )
        .order_by(
            Prediction.created_at.desc()
        )
        .all()
    )

    return predictions