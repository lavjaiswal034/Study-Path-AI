from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.roles import require_role

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


# =========================================================
# REQUEST SCHEMA
# =========================================================

class CreateClassRequest(BaseModel):
    class_name: str
    academic_year_id: int
    semester_id: int
    branch_id: int
    teacher_id: int
    subject_id: int


# =========================================================
# ADMIN STATUS
# =========================================================

@router.get("/status")
def admin_status(
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    return {
        "message": "Admin module is working"
    }


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    return get_admin_dashboard_data(
        db=db,
    )


# =========================================================
# ALL USERS
# =========================================================

@router.get("/users")
def all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    users = get_all_users(db)

    return {
        "total_users": len(users),
        "users": users,
    }


# =========================================================
# PENDING USERS
# =========================================================

@router.get("/pending-users")
def pending_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    users = get_pending_users(db)

    return {
        "total_pending": len(users),
        "users": users,
    }


# =========================================================
# APPROVE USER
# =========================================================

@router.patch("/users/{user_id}/approve")
def approve_pending_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = approve_user(
        db=db,
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


# =========================================================
# REJECT USER
# =========================================================

@router.patch("/users/{user_id}/reject")
def reject_pending_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = reject_user(
        db=db,
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


# =========================================================
# ACTIVATE USER
# =========================================================

@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = set_user_active_status(
        db=db,
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


# =========================================================
# DEACTIVATE USER
# =========================================================

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = set_user_active_status(
        db=db,
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


# =========================================================
# DELETE USER
# =========================================================

@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    user = delete_user(
        db=db,
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


# =========================================================
# ALL CLASSES
# =========================================================

@router.get("/classes")
def admin_get_classes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    classes = get_all_classes(db)

    return {
        "total_classes": len(classes),
        "classes": classes,
    }


# =========================================================
# CLASS DETAILS
# =========================================================

@router.get("/classes/{class_id}")
def admin_class_details(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    class_data = get_class_details(
        db=db,
        class_id=class_id,
    )

    if not class_data:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    return class_data


# =========================================================
# CREATE CLASS
# =========================================================

@router.post("/classes")
def admin_create_class(
    request: CreateClassRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):

    teacher = get_teacher_by_id(
        db=db,
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

    try:
        class_data = create_class(
            db=db,
            class_name=request.class_name,
            academic_year_id=request.academic_year_id,
            semester_id=request.semester_id,
            branch_id=request.branch_id,
            teacher_id=request.teacher_id,
            subject_id=request.subject_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "Class created successfully",
        "class": class_data,
    }


# =========================================================
# DELETE CLASS
# =========================================================

@router.delete("/classes/{class_id}")
def admin_delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("admin")
    ),
):
    class_data = delete_class(
        db=db,
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