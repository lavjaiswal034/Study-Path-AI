from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.roles import require_role
from app.api.v1.auth import users_db
from app.services.admin_service import (
    get_admin_dashboard_data,
    get_pending_users,
    get_all_users,
    get_all_classes,
    get_class_details,
    approve_user,
    reject_user,
    set_user_active_status,
    delete_user,
    create_class,
    get_teacher_by_id,
    delete_class,
)
router = APIRouter()

classes_db = {}
class CreateClassRequest(BaseModel):
    class_name: str
    subject: str
    teacher_id: int

@router.get("/status")
def admin_status(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    return {
        "message": "Admin module is working"
    }


@router.get("/dashboard")
def admin_dashboard(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    return get_admin_dashboard_data(
        users_db=users_db,
        classes_db=classes_db,
    )
@router.get("/classes/{class_id}")
def admin_class_details(
    class_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    class_data = get_class_details(
        classes_db=classes_db,
        users_db=users_db,
        class_id=class_id,
    )

    if not class_data:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    return class_data

@router.get("/pending-users")
def pending_users(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    users = get_pending_users(users_db)

    return {
        "total_pending": len(users),
        "users": users,
    }


@router.patch("/users/{user_id}/approve")
def approve_pending_user(
    user_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = approve_user(
        users_db=users_db,
        user_id=user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User approved successfully",
        "user": user,
    }

@router.delete("/classes/{class_id}")
def admin_delete_class(
    class_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    class_data = delete_class(
        classes_db=classes_db,
        class_id=class_id,
    )

    if not class_data:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    return {
        "message": "Class deleted successfully",
        "class": class_data,
    }

@router.get("/classes")
def admin_get_classes(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    classes = get_all_classes(classes_db)

    return {
        "total_classes": len(classes),
        "classes": classes,
    }

@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = set_user_active_status(
        users_db=users_db,
        user_id=user_id,
        is_active=True,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User activated successfully",
        "user": user,
    }


@router.post("/classes")
def admin_create_class(
    request: CreateClassRequest,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    teacher = get_teacher_by_id(
        users_db=users_db,
        teacher_id=request.teacher_id,
    )

    if not teacher:
        raise HTTPException(
            status_code=400,
            detail=(
                "Teacher not found, not approved, "
                "or account is inactive"
            ),
        )

    class_id = len(classes_db) + 1

    class_data = create_class(
        classes_db=classes_db,
        class_id=class_id,
        class_name=request.class_name,
        subject=request.subject,
        teacher_id=request.teacher_id,
    )

    return {
        "message": "Class created successfully",
        "class": class_data,
    }

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = set_user_active_status(
        users_db=users_db,
        user_id=user_id,
        is_active=False,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User deactivated successfully",
        "user": user,
    }
@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = delete_user(
        users_db=users_db,
        user_id=user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found or admin cannot be deleted",
        )

    return {
        "message": "User deleted successfully",
        "user": user,
    }

@router.get("/users")
def all_users(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    users = get_all_users(users_db)

    return {
        "total_users": len(users),
        "users": users,
    }


@router.patch("/users/{user_id}/reject")
def reject_pending_user(
    user_id: int,
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = reject_user(
        users_db=users_db,
        user_id=user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User rejected successfully",
        "user": user,
    }