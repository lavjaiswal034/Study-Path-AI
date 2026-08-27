from datetime import datetime

from pydantic import BaseModel


class TeacherAssignmentResponse(BaseModel):
    id: int
    teacher_id: int

    class_id: int
    class_name: str

    subject_id: int
    subject_name: str
    subject_code: str


class TeacherStudentResponse(BaseModel):
    student_id: int
    student_code: str
    name: str
    email: str
    roll_number: str | None
    branch: str | None
    enrollment_status: str


class TeacherClassAnalyticsResponse(BaseModel):
    class_id: int
    total_students: int
    average_score: float
    average_attendance: float

    performance_distribution: dict[str, int]


class TeacherAssessmentResultResponse(BaseModel):
    attempt_id: int
    assessment_id: int

    student_id: int
    student_code: str
    student_name: str
    student_email: str

    score: int
    max_score: int

    status: str
    submitted_at: datetime | None


class TeacherStudentAnalyticsResponse(BaseModel):
    student_id: int
    student_code: str
    student_name: str

    average_score: float
    highest_score: float
    lowest_score: float

    attendance: float

    performance_level: str
    total_assessments: int