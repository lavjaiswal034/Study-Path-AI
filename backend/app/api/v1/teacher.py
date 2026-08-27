from fastapi import APIRouter, Depends

from app.models.assignment import ClassTeacherSubjectAssignment
from app.models.teacher import TeacherProfile
from app.models.user import User
from app.models.class_ import Class
from app.models.subject import Subject

from app.models.enrollment import StudentEnrollment
from app.models.student import StudentProfile
from app.schemas.teacher import (
    TeacherAssignmentResponse,
    TeacherStudentResponse,
)

from app.core.roles import require_role
from app.services.teacher_service import (
    get_teacher_dashboard_data,
)


router = APIRouter()


@router.get("/status")
def teacher_status():
    return {
        "message": "Teacher module is working"
    }


@router.get("/dashboard")
def teacher_dashboard(
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    dashboard = get_teacher_dashboard_data(
        teacher_id=current_user["user_id"]
    )

    return dashboard
@router.get("/classes")
def teacher_classes(
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL.

    classes = [
        {
            "class_id": 1,
            "class_name": "CSE-DS A",
            "subject": "Data Science",
            "student_count": 30,
        },
        {
            "class_id": 2,
            "class_name": "CSE-DS B",
            "subject": "Machine Learning",
            "student_count": 28,
        },
    ]

    return {
        "teacher_id": current_user["user_id"],
        "classes": classes,
    }

@router.get("/classes/{class_id}/students")
def class_students(
    class_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL.

    students = [
        {
            "student_id": 101,
            "name": "Student One",
            "average_score": 78,
            "attendance": 88,
            "risk_level": "low",
        },
        {
            "student_id": 102,
            "name": "Student Two",
            "average_score": 62,
            "attendance": 76,
            "risk_level": "medium",
        },
        {
            "student_id": 103,
            "name": "Student Three",
            "average_score": 41,
            "attendance": 65,
            "risk_level": "high",
        },
    ]

    return {
        "teacher_id": current_user["user_id"],
        "class_id": class_id,
        "students": students,
    }

@router.get("/classes/{class_id}/analytics")
def class_analytics(
    class_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL.

    students = [
        {
            "student_id": 101,
            "average_score": 78,
            "attendance": 88,
        },
        {
            "student_id": 102,
            "average_score": 62,
            "attendance": 76,
        },
        {
            "student_id": 103,
            "average_score": 41,
            "attendance": 65,
        },
    ]

    total_students = len(students)

    average_score = round(
        sum(
            student["average_score"]
            for student in students
        ) / total_students,
        2,
    )

    average_attendance = round(
        sum(
            student["attendance"]
            for student in students
        ) / total_students,
        2,
    )

    high_performers = sum(
        1
        for student in students
        if student["average_score"] >= 75
    )

    medium_performers = sum(
        1
        for student in students
        if 50 <= student["average_score"] < 75
    )

    low_performers = sum(
        1
        for student in students
        if student["average_score"] < 50
    )

    return {
        "teacher_id": current_user["user_id"],
        "class_id": class_id,
        "analytics": {
            "total_students": total_students,
            "average_score": average_score,
            "average_attendance": average_attendance,
            "performance_distribution": {
                "high": high_performers,
                "medium": medium_performers,
                "low": low_performers,
            },
        },
    }

@router.get(
    "/me/classes/{class_id}/students",
    response_model=list[TeacherStudentResponse],
)
def get_my_class_students(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    teacher = (
        db.query(TeacherProfile)
        .filter(
            TeacherProfile.user_id == current_user.id
        )
        .first()
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher profile not found",
        )

    assignment = (
        db.query(ClassTeacherSubjectAssignment)
        .filter(
            ClassTeacherSubjectAssignment.teacher_id
            == teacher.id,
            ClassTeacherSubjectAssignment.class_id
            == class_id,
        )
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this class",
        )

    students = (
        db.query(
            StudentEnrollment,
            StudentProfile,
            User,
        )
        .join(
            StudentProfile,
            StudentEnrollment.student_id
            == StudentProfile.id,
        )
        .join(
            User,
            StudentProfile.user_id
            == User.id,
        )
        .filter(
            StudentEnrollment.class_id
            == class_id,
            StudentEnrollment.enrollment_status
            == "ACTIVE",
        )
        .order_by(
            StudentProfile.roll_number.asc()
        )
        .all()
    )

    return [
        TeacherStudentResponse(
            student_id=enrollment.student_id,
            student_code=student.student_id,
            name=user.name,
            email=user.email,
            roll_number=student.roll_number,
            branch=student.branch,
            enrollment_status=enrollment.enrollment_status,
        )
        for enrollment, student, user in students
    ]


@router.get("/classes/{class_id}/weak-areas")
def class_weak_areas(
    class_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL
    # and student performance records.

    topic_scores = {
        "Python": 68,
        "SQL": 45,
        "Data Structures": 42,
        "Machine Learning": 61,
        "Statistics": 48,
    }

    weak_areas = []

    for topic, score in topic_scores.items():

        if score < 50:

            if score < 40:
                priority = "high"
            else:
                priority = "medium"

            weak_areas.append(
                {
                    "topic": topic,
                    "average_score": score,
                    "priority": priority,
                }
            )

    weak_areas.sort(
        key=lambda item: item["average_score"]
    )

    return {
        "teacher_id": current_user["user_id"],
        "class_id": class_id,
        "weak_areas": weak_areas,
    }

@router.get("/students/{student_id}")
def student_details(
    student_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL,
    # ML service and analytics service.

    return {
        "teacher_id": current_user["user_id"],
        "student": {
            "student_id": student_id,
            "name": "Student One",
            "average_score": 72.0,
            "highest_score": 85.0,
            "lowest_score": 58.0,
            "attendance": 85.0,
            "performance_level": "good",
            "predicted_score": 78.5,
            "risk_level": "low",
            "confidence": 0.80,
            "weak_areas": [
                {
                    "topic": "SQL",
                    "score": 45,
                    "priority": "medium",
                },
                {
                    "topic": "Data Structures",
                    "score": 38,
                    "priority": "high",
                },
            ],
            "learning_roadmap": [
                {
                    "topic": "SQL",
                    "priority": "high",
                    "estimated_hours": 6,
                },
                {
                    "topic": "Data Structures",
                    "priority": "medium",
                    "estimated_hours": 8,
                },
            ],
        },
    }


@router.get("/students/{student_id}/progress")
def student_progress(
    student_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL.

    scores = [
        {
            "assessment": "Test 1",
            "score": 58,
        },
        {
            "assessment": "Test 2",
            "score": 64,
        },
        {
            "assessment": "Test 3",
            "score": 69,
        },
        {
            "assessment": "Test 4",
            "score": 76,
        },
    ]

    first_score = scores[0]["score"]
    last_score = scores[-1]["score"]

    if last_score > first_score:
        trend = "improving"
    elif last_score < first_score:
        trend = "declining"
    else:
        trend = "stable"

    improvement = last_score - first_score

    return {
        "teacher_id": current_user["user_id"],
        "student_id": student_id,
        "progress": {
            "scores": scores,
            "trend": trend,
            "improvement": improvement,
            "current_score": last_score,
        },
    }

@router.get("/alerts")
def teacher_alerts(
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will come from PostgreSQL
    # and the ML prediction service.

    alerts = [
        {
            "student_id": 103,
            "student_name": "Student Three",
            "risk_level": "high",
            "predicted_score": 41.5,
            "attendance": 65,
            "message": (
                "Student requires immediate "
                "academic support."
            ),
        },
        {
            "student_id": 102,
            "student_name": "Student Two",
            "risk_level": "medium",
            "predicted_score": 62.0,
            "attendance": 76,
            "message": (
                "Student may benefit from "
                "additional practice."
            ),
        },
    ]

    return {
        "teacher_id": current_user["user_id"],
        "total_alerts": len(alerts),
        "alerts": alerts,
    }
@router.get("/students/{student_id}/recommendations")
def student_recommendations(
    student_id: int,
    current_user: dict = Depends(
        require_role("teacher")
    ),
):
    # Temporary data.
    # Later this will be generated from
    # ML prediction + analytics + LLM roadmap.

    recommendations = [
        {
            "type": "academic",
            "priority": "high",
            "title": "Focus on SQL",
            "description": (
                "Student has a low SQL score. "
                "Recommend additional SQL practice."
            ),
        },
        {
            "type": "practice",
            "priority": "medium",
            "title": "Practice Data Structures",
            "description": (
                "Student should practice arrays, "
                "linked lists and trees."
            ),
        },
        {
            "type": "study_plan",
            "priority": "medium",
            "title": "Follow Learning Roadmap",
            "description": (
                "Encourage the student to follow "
                "their personalized learning roadmap."
            ),
        },
    ]

    return {
        "teacher_id": current_user["user_id"],
        "student_id": student_id,
        "recommendations": recommendations,
    }