from app.clients.llm_client import generate_learning_roadmap


def generate_fallback_roadmap(
    weak_topics: list[str],
    risk_level: str,
    study_hours_per_day: float,
) -> list[dict]:

    roadmap = []

    if not weak_topics:
        weak_topics = [
            "Python Fundamentals",
            "SQL",
            "Data Structures",
        ]

    for index, topic in enumerate(weak_topics):

        if index == 0:
            priority = "high"
        elif index == 1:
            priority = "medium"
        else:
            priority = "low"

        estimated_hours = max(
            2.0,
            study_hours_per_day * 3
        )

        roadmap.append(
            {
                "topic": topic,
                "priority": priority,
                "estimated_hours": estimated_hours,
                "description": (
                    f"Improve your understanding of {topic} "
                    "through concepts, practice and revision."
                ),
                "resources": [
                    f"Study {topic} fundamentals",
                    f"Practice {topic} problems",
                    f"Revise {topic} concepts",
                ],
            }
        )

    return roadmap


async def create_personalized_roadmap(
    student_id: int,
    predicted_score: float | None,
    risk_level: str,
    weak_topics: list[str],
    study_hours_per_day: float,
) -> dict:

    roadmap_data = {
        "student_id": student_id,
        "predicted_score": predicted_score,
        "risk_level": risk_level,
        "weak_topics": weak_topics,
        "study_hours_per_day": study_hours_per_day,
    }

    # Try the actual LLM service first
    result = await generate_learning_roadmap(
        roadmap_data
    )

    # If LLM service is available
    if result.get("success") is True:
        return result

    # Fallback if LLM service is unavailable
    fallback_roadmap = generate_fallback_roadmap(
        weak_topics=weak_topics,
        risk_level=risk_level,
        study_hours_per_day=study_hours_per_day,
    )

    return {
        "success": True,
        "roadmap": fallback_roadmap,
        "message": (
            "Personalized roadmap generated "
            "using the fallback recommendation engine."
        ),
    }