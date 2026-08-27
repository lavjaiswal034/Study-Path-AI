from pydantic import BaseModel


class StudentEnrollmentCreate(BaseModel):
    class_id: int
    academic_year_id: int


class StudentEnrollmentResponse(BaseModel):
    id: int
    student_id: int
    class_id: int
    academic_year_id: int
    enrollment_status: str