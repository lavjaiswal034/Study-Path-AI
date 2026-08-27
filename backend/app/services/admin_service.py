from sqlalchemy.orm import Session

from app.models.user import User
from app.models.teacher import TeacherProfile
from app.models.student import StudentProfile
from app.models.class_ import Class
from app.models.subject import Subject
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from app.models.branch import Branch
from app.models.assignment import (
    ClassTeacherSubjectAssignment,
)


# =========================================================
# USER MANAGEMENT
# =========================================================

def get_all_users(
    db: Session,
) -> list[dict]:

    users = (
        db.query(User)
        .order_by(User.id.asc())
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "approval_status": user.approval_status,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        for user in users
    ]


def get_pending_users(
    db: Session,
) -> list[dict]:

    users = (
        db.query(User)
        .filter(
            User.approval_status == "PENDING"
        )
        .order_by(User.id.asc())
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "approval_status": user.approval_status,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        for user in users
    ]


def approve_user(
    db: Session,
    user_id: int,
) -> dict | None:

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    user.approval_status = "APPROVED"

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "approval_status": user.approval_status,
        "is_active": user.is_active,
    }


def reject_user(
    db: Session,
    user_id: int,
) -> dict | None:

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    user.approval_status = "REJECTED"

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "approval_status": user.approval_status,
        "is_active": user.is_active,
    }


def set_user_active_status(
    db: Session,
    user_id: int,
    is_active: bool,
) -> dict | None:

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "approval_status": user.approval_status,
        "is_active": user.is_active,
    }


def delete_user(
    db: Session,
    user_id: int,
) -> dict | None:

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    # Never allow admin account deletion
    if user.role == "admin":
        return None

    result = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }

    db.delete(user)
    db.commit()

    return result


def get_teacher_by_id(
    db: Session,
    teacher_id: int,
) -> dict | None:

    teacher = (
        db.query(TeacherProfile)
        .join(
            User,
            TeacherProfile.user_id == User.id,
        )
        .filter(
            TeacherProfile.id == teacher_id,
            User.role == "teacher",
            User.approval_status == "APPROVED",
            User.is_active.is_(True),
        )
        .first()
    )

    if not teacher:
        return None

    return {
        "id": teacher.id,
        "teacher_id": teacher.teacher_id,
        "employee_id": teacher.employee_id,
        "department": teacher.department,
        "user_id": teacher.user_id,
        "name": teacher.user.name,
        "email": teacher.user.email,
    }


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def get_admin_dashboard_data(
    db: Session,
) -> dict:

    users = db.query(User).all()

    total_users = len(users)

    total_students = sum(
        1
        for user in users
        if user.role == "student"
    )

    total_teachers = sum(
        1
        for user in users
        if user.role == "teacher"
    )

    approved_users = sum(
        1
        for user in users
        if user.approval_status == "APPROVED"
    )

    pending_users = sum(
        1
        for user in users
        if user.approval_status == "PENDING"
    )

    rejected_users = sum(
        1
        for user in users
        if user.approval_status == "REJECTED"
    )

    active_users = sum(
        1
        for user in users
        if user.is_active is True
    )

    inactive_users = sum(
        1
        for user in users
        if user.is_active is False
    )

    total_classes = (
        db.query(Class)
        .count()
    )

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "approved_users": approved_users,
        "pending_users": pending_users,
        "rejected_users": rejected_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
    }


# =========================================================
# CLASS MANAGEMENT
# =========================================================

def get_all_classes(
    db: Session,
) -> list[dict]:

    classes = (
        db.query(Class)
        .order_by(Class.id.asc())
        .all()
    )

    result = []

    for class_obj in classes:

        assignments = (
            db.query(
                ClassTeacherSubjectAssignment
            )
            .filter(
                ClassTeacherSubjectAssignment.class_id
                == class_obj.id
            )
            .all()
        )

        result.append(
            {
                "class_id": class_obj.id,
                "class_name": class_obj.name,
                "academic_year_id": class_obj.academic_year_id,
                "semester_id": class_obj.semester_id,
                "branch_id": class_obj.branch_id,
                "assignments": [
                    {
                        "assignment_id": assignment.id,
                        "teacher_id": assignment.teacher_id,
                        "subject_id": assignment.subject_id,
                    }
                    for assignment in assignments
                ],
            }
        )

    return result


def create_class(
    db: Session,
    class_name: str,
    academic_year_id: int,
    semester_id: int,
    branch_id: int,
    teacher_id: int,
    subject_id: int,
) -> dict:

    academic_year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.id == academic_year_id
        )
        .first()
    )

    if not academic_year:
        raise ValueError(
            "Academic year not found"
        )

    semester = (
        db.query(Semester)
        .filter(
            Semester.id == semester_id
        )
        .first()
    )

    if not semester:
        raise ValueError(
            "Semester not found"
        )

    branch = (
        db.query(Branch)
        .filter(
            Branch.id == branch_id
        )
        .first()
    )

    if not branch:
        raise ValueError(
            "Branch not found"
        )

    teacher = (
        db.query(TeacherProfile)
        .join(
            User,
            TeacherProfile.user_id == User.id,
        )
        .filter(
            TeacherProfile.id == teacher_id,
            User.role == "teacher",
            User.approval_status == "APPROVED",
            User.is_active.is_(True),
        )
        .first()
    )

    if not teacher:
        raise ValueError(
            "Teacher not found, not approved, or inactive"
        )

    subject = (
        db.query(Subject)
        .filter(
            Subject.id == subject_id
        )
        .first()
    )

    if not subject:
        raise ValueError(
            "Subject not found"
        )

    class_obj = Class(
        name=class_name,
        academic_year_id=academic_year_id,
        semester_id=semester_id,
        branch_id=branch_id,
    )

    db.add(class_obj)
    db.flush()

    assignment = ClassTeacherSubjectAssignment(
        teacher_id=teacher_id,
        class_id=class_obj.id,
        subject_id=subject_id,
    )

    db.add(assignment)

    db.commit()

    db.refresh(class_obj)

    return {
        "class_id": class_obj.id,
        "class_name": class_obj.name,
        "academic_year_id": class_obj.academic_year_id,
        "semester_id": class_obj.semester_id,
        "branch_id": class_obj.branch_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
    }


def delete_class(
    db: Session,
    class_id: int,
) -> dict | None:

    class_obj = (
        db.query(Class)
        .filter(Class.id == class_id)
        .first()
    )

    if not class_obj:
        return None

    assignments = (
        db.query(
            ClassTeacherSubjectAssignment
        )
        .filter(
            ClassTeacherSubjectAssignment.class_id
            == class_id
        )
        .all()
    )

    result = {
        "class_id": class_obj.id,
        "class_name": class_obj.name,
    }

    for assignment in assignments:
        db.delete(assignment)

    db.delete(class_obj)

    db.commit()

    return result


def get_class_details(
    db: Session,
    class_id: int,
) -> dict | None:

    class_obj = (
        db.query(Class)
        .filter(Class.id == class_id)
        .first()
    )

    if not class_obj:
        return None

    assignments = (
        db.query(
            ClassTeacherSubjectAssignment
        )
        .filter(
            ClassTeacherSubjectAssignment.class_id
            == class_id
        )
        .all()
    )

    assignment_data = []

    for assignment in assignments:

        teacher = (
            db.query(TeacherProfile)
            .filter(
                TeacherProfile.id
                == assignment.teacher_id
            )
            .first()
        )

        subject = (
            db.query(Subject)
            .filter(
                Subject.id
                == assignment.subject_id
            )
            .first()
        )

        assignment_data.append(
            {
                "assignment_id": assignment.id,
                "teacher": (
                    {
                        "id": teacher.id,
                        "teacher_id": teacher.teacher_id,
                        "name": teacher.user.name,
                        "email": teacher.user.email,
                    }
                    if teacher
                    else None
                ),
                "subject": (
                    {
                        "id": subject.id,
                        "name": subject.name,
                        "code": subject.code,
                    }
                    if subject
                    else None
                ),
            }
        )

    return {
        "class_id": class_obj.id,
        "class_name": class_obj.name,
        "academic_year_id": class_obj.academic_year_id,
        "semester_id": class_obj.semester_id,
        "branch_id": class_obj.branch_id,
        "assignments": assignment_data,
    }