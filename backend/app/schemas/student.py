from pydantic import BaseModel


class StudentProfileCreate(BaseModel):
    student_id: str
    roll_number: str | None = None
    branch: str | None = None


class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    student_id: str
    roll_number: str | None
    branch: str | None