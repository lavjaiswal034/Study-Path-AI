from datetime import datetime


def create_notification(
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "info",
) -> dict:

    return {
        "id": 1,
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": notification_type,
        "is_read": False,
        "created_at": datetime.utcnow().isoformat(),
    }


def create_performance_notification(
    user_id: int,
    predicted_score: float,
    risk_level: str,
) -> dict:

    if risk_level == "high":
        title = "Performance Alert"
        message = (
            "Your predicted performance indicates "
            "that you may need additional study support."
        )
        notification_type = "warning"

    elif risk_level == "medium":
        title = "Performance Update"
        message = (
            "Your performance is moderate. "
            "Following your personalized learning "
            "roadmap can help you improve."
        )
        notification_type = "info"

    else:
        title = "Great Progress!"
        message = (
            "Your predicted performance looks good. "
            "Keep following your learning roadmap."
        )
        notification_type = "success"

    return create_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
    )