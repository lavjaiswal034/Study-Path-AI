import httpx

from app.core.config import settings


async def predict_with_ml(data: dict) -> dict:
    """
    Sends student data to the separate ML service.
    """

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                f"{settings.ml_service_url}/predict",
                json=data,
            )

            response.raise_for_status()

            result = response.json()

            return {
                "predicted_score": result.get(
                    "predicted_score"
                ),
                "risk_level": result.get(
                    "risk_level",
                    "unknown",
                ),
                "confidence": result.get(
                    "confidence"
                ),
            }

    except httpx.HTTPError as error:

        return {
            "success": False,
            "error": str(error),
        }