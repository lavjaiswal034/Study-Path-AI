def get_admin_dashboard_data(
    users_db: dict,
    classes_db: dict,
) -> dict:

    users = list(users_db.values())

    total_users = len(users)

    total_students = sum(
        1
        for user in users
        if user.get("role") == "student"
    )

    total_teachers = sum(
        1
        for user in users
        if user.get("role") == "teacher"
    )

    approved_users = sum(
        1
        for user in users
        if user.get("approval_status") == "approved"
    )

    pending_users = sum(
        1
        for user in users
        if user.get("approval_status") == "pending"
    )

    rejected_users = sum(
        1
        for user in users
        if user.get("approval_status") == "rejected"
    )

    active_users = sum(
        1
        for user in users
        if user.get("is_active", True) is True
    )

    inactive_users = sum(
        1
        for user in users
        if user.get("is_active") is False
    )

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": len(classes_db),
        "approved_users": approved_users,
        "pending_users": pending_users,
        "rejected_users": rejected_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
    }


def get_pending_users(
    users_db: dict,
) -> list[dict]:

    pending_users = []

    for user in users_db.values():

        if user.get("approval_status") == "pending":
            pending_users.append(user)

    return pending_users
def set_user_active_status(
    users_db: dict,
    user_id: int,
    is_active: bool,
) -> dict | None:

    for email, user in users_db.items():

        if user.get("id") == user_id:

            user["is_active"] = is_active

            users_db[email] = user

            return user

    return None

def get_all_users(
    users_db: dict,
) -> list[dict]:

    return list(users_db.values())

def approve_user(
    users_db: dict,
    user_id: int,
) -> dict | None:

    for email, user in users_db.items():

        if user.get("id") == user_id:

            user["approval_status"] = "approved"

            users_db[email] = user

            return user

    return None

def delete_user(
    users_db: dict,
    user_id: int,
) -> dict | None:

    for email, user in list(users_db.items()):

        if user.get("id") == user_id:

            # Prevent deleting an admin account.
            if user.get("role") == "admin":
                return None

            deleted_user = users_db.pop(email)

            return deleted_user

    return None
def get_teacher_by_id(
    users_db: dict,
    teacher_id: int,
) -> dict | None:

    for user in users_db.values():

        if (
            user.get("id") == teacher_id
            and user.get("role") == "teacher"
            and user.get("approval_status") == "approved"
            and user.get("is_active", True) is True
        ):
            return user

    return None

def get_all_classes(
    classes_db: dict,
) -> list[dict]:

    return list(classes_db.values())

def create_class(
    classes_db: dict,
    class_id: int,
    class_name: str,
    subject: str,
    teacher_id: int,
) -> dict:

    class_data = {
        "class_id": class_id,
        "class_name": class_name,
        "subject": subject,
        "teacher_id": teacher_id,
        "student_ids": [],
    }

    classes_db[class_id] = class_data

    return class_data

def reject_user(
    users_db: dict,
    user_id: int,
) -> dict | None:

    for email, user in users_db.items():

        if user.get("id") == user_id:

            user["approval_status"] = "rejected"

            users_db[email] = user

            return user

    return None
def delete_class(
    classes_db: dict,
    class_id: int,
) -> dict | None:

    if class_id not in classes_db:
        return None

    deleted_class = classes_db.pop(class_id)

    return deleted_class

def get_class_details(
    classes_db: dict,
    users_db: dict,
    class_id: int,
) -> dict | None:

    class_data = classes_db.get(class_id)

    if not class_data:
        return None

    teacher = None

    for user in users_db.values():
        if user.get("id") == class_data.get("teacher_id"):
            teacher = {
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
            }
            break

    return {
        "class_id": class_data.get("class_id"),
        "class_name": class_data.get("class_name"),
        "subject": class_data.get("subject"),
        "teacher": teacher,
        "student_ids": class_data.get(
            "student_ids",
            [],
        ),
        "student_count": len(
            class_data.get("student_ids", [])
        ),
    }