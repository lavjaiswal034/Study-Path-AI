from fastapi import APIRouter, Depends, HTTPException

from app.clients.ml_client import predict_with_ml
from app.core.roles import require_role
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.notification_service import (
    create_performance_notification,
)

router = APIRouter()


@router.get("/status")
def prediction_status():
    return {
        "message": "Prediction module is working"
    }


@router.post(
    "/student",
    response_model=PredictionResponse,
)
async def predict_student(
    request: PredictionRequest,
    current_user: dict = Depends(
        require_role("student")
    ),
):
    ml_data = {
        "student_id": current_user["user_id"],
        "attendance": request.attendance,
        "assignment_score": request.assignment_score,
        "previous_score": request.previous_score,
        "study_hours": request.study_hours,
    }

    result = await predict_with_ml(ml_data)

    if result.get("success") is False:
        raise HTTPException(
            status_code=503,
            detail="ML service is currently unavailable",
        )

    # Create a notification based on the prediction
    notification = create_performance_notification(
        user_id=current_user["user_id"],
        predicted_score=result.get(
            "predicted_score",
            0,
        ),
        risk_level=result.get(
            "risk_level",
            "unknown",
        ),
    )

    return {
        "student_id": current_user["user_id"],
        "prediction": result,
        "notification": notification,
    }