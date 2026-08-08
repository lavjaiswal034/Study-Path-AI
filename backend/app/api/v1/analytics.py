from fastapi import APIRouter, Depends

from app.core.roles import require_role
from app.schemas.analytics import (
    StudentAnalyticsResponse,
    ClassAnalyticsResponse,
)
from app.services.analytics_service import (
    calculate_student_analytics,
    calculate_class_analytics,
    detect_weak_areas,
)


router = APIRouter()


@router.get("/status")
def analytics_status():
    return {
        "message": "Analytics module is working"
    }


@router.get(
    "/student",
    response_model=StudentAnalyticsResponse,
)
def student_analytics(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    scores = [65, 72, 68, 80, 75]
    attendance = 85.0

    analytics = calculate_student_analytics(
        scores=scores,
        attendance=attendance,
    )

    return {
        "student_id": current_user["user_id"],
        "analytics": analytics,
    }


@router.get(
    "/class",
    response_model=ClassAnalyticsResponse,
)
def class_analytics(
    current_user: dict = Depends(
        require_role("teacher", "admin")
    ),
):
    students = [
        {
            "average_score": 72,
            "attendance": 85,
        },
        {
            "average_score": 68,
            "attendance": 78,
        },
        {
            "average_score": 81,
            "attendance": 91,
        },
    ]

    analytics = calculate_class_analytics(
        students=students,
    )

    return {
        "analytics": analytics,
    }


@router.get("/student/weak-areas")
def student_weak_areas(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    topic_scores = {
        "Python": 72,
        "SQL": 45,
        "Data Structures": 38,
        "Machine Learning": 67,
        "Statistics": 42,
    }

    weak_areas = detect_weak_areas(
        topic_scores=topic_scores,
        threshold=50,
    )

    return {
        "student_id": current_user["user_id"],
        "weak_areas": weak_areas,
    }