def get_teacher_dashboard_data(
    teacher_id: int,
) -> dict:

    # Temporary data.
    # Later this will come from PostgreSQL.

    classes = [
        {
            "class_id": 1,
            "class_name": "CSE-DS A",
            "student_count": 30,
        },
        {
            "class_id": 2,
            "class_name": "CSE-DS B",
            "student_count": 28,
        },
    ]

    return {
        "teacher_id": teacher_id,
        "total_classes": len(classes),
        "total_students": sum(
            class_data["student_count"]
            for class_data in classes
        ),
        "classes": classes,
    }