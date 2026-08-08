from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    name: str
    email: EmailStr


class TeacherResponse(TeacherBase):
    id: int