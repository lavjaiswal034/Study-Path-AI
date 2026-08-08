from fastapi import APIRouter, Depends, HTTPException

from app.core.roles import require_role


router = APIRouter()


# Temporary class data.
# Later this will come from PostgreSQL/database layer.
classes_db = [
    {
        "id": 1,
        "name": "CSE - Data Science",
        "section": "A",
        "teacher_id": 1,
        "academic_year": "2026-27",
    },
    {
        "id": 2,
        "name": "CSE - Data Science",
        "section": "B",
        "teacher_id": 1,
        "academic_year": "2026-27",
    },
    {
        "id": 3,
        "name": "Computer Science",
        "section": "A",
        "teacher_id": 2,
        "academic_year": "2026-27",
    },
]


students_db = [
    {
        "id": 1,
        "name": "Student One",
        "email": "student1@test.com",
        "class_id": 1,
    },
    {
        "id": 2,
        "name": "Student Two",
        "email": "student2@test.com",
        "class_id": 1,
    },
    {
        "id": 3,
        "name": "Student Three",
        "email": "student3@test.com",
        "class_id": 2,
    },
]


@router.get("")
def get_my_classes(
    current_user: dict = Depends(require_role("teacher")),
):
    teacher_id = current_user["user_id"]

    teacher_classes = [
        class_data
        for class_data in classes_db
        if class_data["teacher_id"] == teacher_id
    ]

    return {
        "teacher_id": teacher_id,
        "total_classes": len(teacher_classes),
        "classes": teacher_classes,
    }


@router.get("/{class_id}")
def get_class(
    class_id: int,
    current_user: dict = Depends(require_role("teacher")),
):
    teacher_id = current_user["user_id"]

    class_data = next(
        (
            class_item
            for class_item in classes_db
            if class_item["id"] == class_id
            and class_item["teacher_id"] == teacher_id
        ),
        None,
    )

    if not class_data:
        raise HTTPException(
            status_code=404,
            detail="Class not found or you do not have access to this class",
        )

    return class_data


@router.get("/{class_id}/students")
def get_class_students(
    class_id: int,
    current_user: dict = Depends(require_role("teacher")),
):
    teacher_id = current_user["user_id"]

    class_data = next(
        (
            class_item
            for class_item in classes_db
            if class_item["id"] == class_id
            and class_item["teacher_id"] == teacher_id
        ),
        None,
    )

    if not class_data:
        raise HTTPException(
            status_code=404,
            detail="Class not found or you do not have access to this class",
        )

    students = [
        student
        for student in students_db
        if student["class_id"] == class_id
    ]

    return {
        "class": class_data,
        "total_students": len(students),
        "students": students,
    }