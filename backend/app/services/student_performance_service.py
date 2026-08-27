from sqlalchemy.orm import Session

from app.models.attempt import AssessmentAttempt


def get_student_previous_score(
    db: Session,
    student_id: int,
) -> float:
    """
    Gets the average score from the student's
    previously submitted assessments.
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
        return 0.0

    return round(
        sum(scores) / len(scores),
        2,
    )