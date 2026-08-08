from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from jose import JWTError, jwt

from app.core.config import settings


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    try:
        password_hasher.verify(
            hashed_password,
            plain_password
        )

        return True

    except Exception:
        return False


def create_access_token(
    user_id: int,
    role: str,
    expires_minutes: int = 60
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        return payload

    except JWTError:

        raise ValueError(
            "Invalid or expired token"
        )