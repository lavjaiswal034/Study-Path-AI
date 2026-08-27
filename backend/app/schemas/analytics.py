from pydantic import BaseModel


class PerformanceDistribution(BaseModel):
    high: int
    medium: int
    low: int


class StudentAnalytics(BaseModel):
    average_score: float
    highest_score: float
    lowest_score: float
    attendance: float
    performance_level: str
    total_assessments: int


class ClassAnalytics(BaseModel):
    total_students: int
    average_score: float
    average_attendance: float
    performance_distribution: PerformanceDistribution

def calculate_previous_score(
    scores: list[float],
) -> float:
    """
    Calculates the student's previous average score
    from completed assessments.
    """

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2,
    )

class StudentAnalyticsResponse(BaseModel):
    student_id: int
    analytics: StudentAnalytics


class ClassAnalyticsResponse(BaseModel):
    analytics: ClassAnalytics