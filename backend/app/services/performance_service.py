from sqlalchemy.orm import Session

from app.models.attempt import AssessmentAttempt


def get_student_performance_summary(
    db: Session,
    student_id: int,
) -> dict:
    """
    Returns the student's performance summary
    from submitted assessment attempts.
    """

    attempts = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.student_id == student_id,
            AssessmentAttempt.status == "SUBMITTED",
        )
        .all()
    )

    scores = [
        attempt.score
        for attempt in attempts
        if attempt.score is not None
    ]

    if not scores:
        return {
            "previous_score": 0.0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
            "total_assessments": 0,
        }

    return {
        "previous_score": round(
            sum(scores) / len(scores),
            2,
        ),
        "average_score": round(
            sum(scores) / len(scores),
            2,
        ),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "total_assessments": len(scores),
    }