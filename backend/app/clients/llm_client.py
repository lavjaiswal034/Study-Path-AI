import httpx

from app.core.config import settings


async def generate_learning_roadmap(data: dict) -> dict:
    """
    Sends student performance information
    to the separate LLM service.
    """

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                f"{settings.llm_service_url}/generate",
                json=data,
            )

            response.raise_for_status()

            result = response.json()

            return {
                "success": True,
                "roadmap": result.get("roadmap", []),
                "message": result.get(
                    "message",
                    "Learning roadmap generated successfully",
                ),
            }

    except httpx.HTTPError as error:

        return {
            "success": False,
            "roadmap": [],
            "message": str(error),
        }