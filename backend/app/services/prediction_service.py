from app.clients.ml_client import predict_with_ml


async def predict_student_performance(
    features: dict,
    final_exam_max_marks: float | None = None,
) -> dict:
    """
    Sends the final engineered feature set to the ML service
    and returns the prediction result.
    """

    data = {
        **features,
        "final_exam_max_marks": final_exam_max_marks,
    }

    result = await predict_with_ml(data)

    predicted_percentage = result.get(
        "predicted_percentage"
    )

    if predicted_percentage is None:
        raise RuntimeError(
            "ML service did not return predicted_percentage"
        )

    return {
        "predicted_percentage": float(
            predicted_percentage
        ),
        "predicted_marks": result.get(
            "predicted_marks"
        ),
        "final_exam_max_marks": result.get(
            "final_exam_max_marks"
        ),
        "model_version": result.get(
            "model_version"
        ),
        "feature_set_version": result.get(
            "feature_set_version"
        ),
        "risk_level": result.get(
            "risk_level"
        ),
        "confidence_or_uncertainty": result.get(
            "confidence_or_uncertainty"
        ),
        "prediction_timestamp": result.get(
            "prediction_timestamp"
        ),
    }