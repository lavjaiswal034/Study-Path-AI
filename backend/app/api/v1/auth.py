from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    register_user,
)


router = APIRouter()


# Temporary storage.
# Later this will be replaced by PostgreSQL.
users_db = {}


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(request: RegisterRequest):

    if request.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Admin cannot be created through normal registration.
    if request.role.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin registration is not allowed",
        )

    user_id = len(users_db) + 1

    user = register_user(
        user_id=user_id,
        name=request.name,
        email=request.email,
        password=request.password,
        role=request.role.value,
    )

    # NEW:
    # Every newly registered user requires
    # administrator approval.
    user["approval_status"] = "pending"

    users_db[request.email] = user

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(request: LoginRequest):

    user = users_db.get(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # NEW:
    # User cannot login until administrator approves.
    if user.get("approval_status") == "pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Your account is pending administrator approval."
            ),
        )

    # NEW:
    # Rejected users cannot login.
    if user.get("approval_status") == "rejected":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Your account registration was rejected "
                "by the administrator."
            ),
        )
    if user.get("is_active") is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated by the administrator.",
        )

    token = authenticate_user(
        user=user,
        password=request.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Authenticated user",
        "user": current_user,
    }