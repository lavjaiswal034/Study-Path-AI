import httpx

from app.core.config import settings


async def predict_with_ml(data: dict) -> dict:
    """
    Sends engineered student features to the ML service.
    """

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                f"{settings.ml_service_url}/api/v1/predictions/run",
                json=data,
            )

            response.raise_for_status()

            result = response.json()

            return {
                "predicted_percentage": result.get(
                    "predicted_percentage"
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

    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"ML service returned HTTP "
            f"{error.response.status_code}: "
            f"{error.response.text}"
        ) from error

    except httpx.RequestError as error:
        raise RuntimeError(
            f"Unable to connect to ML service: {error}"
        ) from error