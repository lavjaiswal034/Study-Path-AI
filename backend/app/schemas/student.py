from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    name: str
    email: EmailStr


class StudentResponse(StudentBase):
    id: int