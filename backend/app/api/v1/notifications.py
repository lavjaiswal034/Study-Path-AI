from fastapi import APIRouter, Depends

from app.core.roles import require_role
from app.services.notification_service import (
    create_performance_notification,
)


router = APIRouter()


@router.get("/status")
def notification_status():
    return {
        "message": "Notifications module is working"
    }

@router.patch("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user: dict = Depends(
        require_role("student")
    ),
):
    return {
        "notification_id": notification_id,
        "user_id": current_user["user_id"],
        "is_read": True,
        "message": "Notification marked as read",
    }

@router.get("/")
def get_notifications(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    # Temporary notification data.
    # Later this will come from PostgreSQL.

    notification = create_performance_notification(
        user_id=current_user["user_id"],
        predicted_score=78.5,
        risk_level="low",
    )

    return {
        "user_id": current_user["user_id"],
        "notifications": [
            notification
        ],
    }