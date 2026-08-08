from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    approval_status: ApprovalStatus


class TokenResponse(BaseModel):
    access_token: str
    token_type: str