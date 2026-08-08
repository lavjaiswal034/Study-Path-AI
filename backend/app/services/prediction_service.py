def predict_student_performance(
    attendance: float,
    assignment_score: float,
    previous_score: float,
    study_hours: float,
):
    """
    Temporary prediction service.

    Later this function will load the trained ML model
    and return the actual model prediction.
    """

    score = (
        attendance * 0.20
        + assignment_score * 0.30
        + previous_score * 0.30
        + min(study_hours * 10, 100) * 0.20
    )

    score = round(score, 2)

    if score >= 75:
        risk_level = "low"
    elif score >= 50:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "predicted_score": score,
        "risk_level": risk_level,
        "confidence": 0.80,
    }