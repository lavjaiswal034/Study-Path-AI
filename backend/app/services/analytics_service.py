def calculate_student_analytics(
    scores: list[float],
    attendance: float,
) -> dict:

    if scores:
        average_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
    else:
        average_score = 0.0
        highest_score = 0.0
        lowest_score = 0.0

    if average_score >= 75:
        performance_level = "excellent"
    elif average_score >= 60:
        performance_level = "good"
    elif average_score >= 40:
        performance_level = "average"
    else:
        performance_level = "needs_improvement"

    return {
        "average_score": round(average_score, 2),
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "attendance": attendance,
        "performance_level": performance_level,
        "total_assessments": len(scores),
    }


def calculate_class_analytics(
    students: list[dict],
) -> dict:

    if not students:
        return {
            "total_students": 0,
            "average_score": 0.0,
            "average_attendance": 0.0,
            "performance_distribution": {
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        }

    total_score = sum(
        student.get("average_score", 0)
        for student in students
    )

    total_attendance = sum(
        student.get("attendance", 0)
        for student in students
    )

    count = len(students)

    high_performers = sum(
        1
        for student in students
        if student.get("average_score", 0) >= 75
    )

    medium_performers = sum(
        1
        for student in students
        if 50 <= student.get("average_score", 0) < 75
    )

    low_performers = sum(
        1
        for student in students
        if student.get("average_score", 0) < 50
    )

    return {
        "total_students": count,
        "average_score": round(
            total_score / count,
            2,
        ),
        "average_attendance": round(
            total_attendance / count,
            2,
        ),
        "performance_distribution": {
            "high": high_performers,
            "medium": medium_performers,
            "low": low_performers,
        },
    }


def detect_weak_areas(
    topic_scores: dict[str, float],
    threshold: float = 50.0,
) -> list[dict]:

    weak_areas = []

    for topic, score in topic_scores.items():

        if score < threshold:

            if score < 40:
                priority = "high"
            else:
                priority = "medium"

            weak_areas.append(
                {
                    "topic": topic,
                    "score": score,
                    "priority": priority,
                }
            )

    weak_areas.sort(
        key=lambda item: item["score"]
    )

    return weak_areas