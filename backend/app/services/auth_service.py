from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def register_user(
    user_id: int,
    name: str,
    email: str,
    password: str,
    role: str,
):
    hashed_password = hash_password(password)

    return {
        "id": user_id,
        "name": name,
        "email": email,
        "password_hash": hashed_password,
        "role": role,
    }


def authenticate_user(
    user: dict,
    password: str,
):
    if not user:
        return None

    if not verify_password(
        password,
        user["password_hash"],
    ):
        return None

    token = create_access_token(
        user_id=user["id"],
        role=user["role"],
    )

    return token