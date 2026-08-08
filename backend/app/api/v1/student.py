from fastapi import APIRouter, Depends

from app.core.roles import require_role


router = APIRouter()


# Temporary student data.
# Later this will come from PostgreSQL.
students_db = {
    1: {
        "id": 1,
        "name": "Student One",
        "email": "student1@test.com",
        "class_id": 1,
        "roll_number": "DS001",
    },
    2: {
        "id": 2,
        "name": "Student Two",
        "email": "student2@test.com",
        "class_id": 1,
        "roll_number": "DS002",
    },
    3: {
        "id": 3,
        "name": "Student Three",
        "email": "student3@test.com",
        "class_id": 2,
        "roll_number": "DS003",
    },
}


@router.get("/status")
def student_status(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    return {
        "message": "Student module is working",
        "user": current_user,
    }


@router.get("/profile")
def get_student_profile(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    student_id = current_user["user_id"]

    student = students_db.get(student_id)

    if not student:
        return {
            "message": "Student profile not found",
            "user_id": student_id,
        }

    return {
        "student": student,
    }


@router.get("/dashboard")
def get_student_dashboard(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    student_id = current_user["user_id"]

    student = students_db.get(student_id)

    return {
        "student_id": student_id,
        "role": current_user["role"],
        "student": student,
        "performance": {
            "average_score": 0,
            "attendance": 0,
            "completed_topics": 0,
        },
        "prediction": {
            "status": "not_available",
        },
        "learning_path": {
            "status": "not_generated",
        },
    }

@router.get("/performance")
def get_student_performance(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    student_id = current_user["user_id"]

    return {
        "student_id": student_id,
        "performance": {
            "average_score": 0,
            "subject_scores": {},
            "attendance_percentage": 0,
            "assignments_completed": 0,
            "assignments_total": 0,
        },
        "message": "Performance data will be connected to the database",
    }


@router.get("/progress")
def get_student_progress(
    current_user: dict = Depends(
        require_role("student")
    ),
):
    student_id = current_user["user_id"]

    return {
        "student_id": student_id,
        "progress": {
            "completed_topics": [],
            "in_progress_topics": [],
            "pending_topics": [],
            "overall_progress_percentage": 0,
        },
        "message": "Progress data will be connected to the database",
    }