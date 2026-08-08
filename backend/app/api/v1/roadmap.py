from fastapi import APIRouter, Depends, HTTPException

from app.core.roles import require_role
from app.schemas.roadmap import (
    RoadmapRequest,
    RoadmapResponse,
)
from app.services.analytics_service import detect_weak_areas
from app.services.roadmap_service import (
    create_personalized_roadmap,
)


router = APIRouter()


@router.get("/status")
def roadmap_status():
    return {
        "message": "Learning roadmap module is working"
    }


@router.post(
    "/generate",
    response_model=RoadmapResponse,
)
async def generate_roadmap(
    request: RoadmapRequest,
    current_user: dict = Depends(
        require_role("student")
    ),
):
    if request.student_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only generate a roadmap for yourself",
        )

    # Temporary topic scores.
    # Later these will come from the database.
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

    weak_topics = [
        area["topic"]
        for area in weak_areas
    ]

    result = await create_personalized_roadmap(
        student_id=request.student_id,
        predicted_score=request.predicted_score,
        risk_level=request.risk_level,
        weak_topics=weak_topics,
        study_hours_per_day=request.study_hours_per_day,
    )

    if result.get("success") is False:
        raise HTTPException(
            status_code=503,
            detail="LLM service is currently unavailable",
        )

    return {
        "student_id": request.student_id,
        "roadmap": result.get("roadmap", []),
        "message": result.get(
            "message",
            "Learning roadmap generated successfully",
        ),
    }