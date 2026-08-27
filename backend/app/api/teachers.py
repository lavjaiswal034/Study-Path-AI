from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.assignment import ClassTeacherSubjectAssignment
from app.models.teacher import TeacherProfile
from app.models.user import User
from app.schemas.teacher import TeacherAssignmentResponse

from app.models.assessment import Assessment
from app.models.attempt import AssessmentAttempt
from app.models.student import StudentProfile
from app.models.enrollment import StudentEnrollment

from app.models.class_ import Class
from app.models.subject import Subject


from app.services.analytics_service import (
    calculate_student_analytics,
    calculate_class_analytics,
)

from app.schemas.teacher import (
    TeacherAssignmentResponse,
    TeacherStudentResponse,
    TeacherAssessmentResultResponse,
    TeacherStudentAnalyticsResponse,
    TeacherClassAnalyticsResponse,
)



router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
)


@router.get(
    "/me/assignments",
    response_model=list[TeacherAssignmentResponse],
)
def get_my_assignments(
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
        .filter(TeacherProfile.user_id == current_user.id)
        .first()
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher profile not found",
        )

    assignments = (
        db.query(
            ClassTeacherSubjectAssignment,
            Class.name.label("class_name"),
            Subject.name.label("subject_name"),
            Subject.code.label("subject_code"),
        )
        .join(
            Class,
            ClassTeacherSubjectAssignment.class_id == Class.id,
        )
        .join(
            Subject,
            ClassTeacherSubjectAssignment.subject_id == Subject.id,
        )
        .filter(
            ClassTeacherSubjectAssignment.teacher_id == teacher.id
        )
        .all()
    )

    return [
        TeacherAssignmentResponse(
            id=assignment.id,
            teacher_id=assignment.teacher_id,
            class_id=assignment.class_id,
            class_name=class_name,
            subject_id=assignment.subject_id,
            subject_name=subject_name,
            subject_code=subject_code,
        )
        for assignment, class_name, subject_name, subject_code in assignments
    ]


@router.get(
    "/me/classes/{class_id}/analytics",
    response_model=TeacherClassAnalyticsResponse,
)
def get_class_analytics(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------
    # 1. Make sure user is a teacher
    # -----------------------------------------

    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    # -----------------------------------------
    # 2. Find teacher profile
    # -----------------------------------------

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

    # -----------------------------------------
    # 3. Verify teacher is assigned to class
    # -----------------------------------------

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

    # -----------------------------------------
    # 4. Get active students
    # -----------------------------------------

    enrollments = (
        db.query(StudentEnrollment)
        .filter(
            StudentEnrollment.class_id == class_id,
            StudentEnrollment.enrollment_status
            == "ACTIVE",
        )
        .all()
    )

    students = []

    # -----------------------------------------
    # 5. Calculate each student's score
    # -----------------------------------------

    for enrollment in enrollments:

        attempts = (
            db.query(AssessmentAttempt)
            .join(
                Assessment,
                AssessmentAttempt.assessment_id
                == Assessment.id,
            )
            .filter(
                AssessmentAttempt.student_id
                == enrollment.student_id,
                AssessmentAttempt.status
                == "SUBMITTED",
                Assessment.teacher_id
                == teacher.id,
                Assessment.class_id
                == class_id,
            )
            .all()
        )

        scores = [
            float(attempt.score or 0)
            for attempt in attempts
        ]

        if scores:
            average_score = (
                sum(scores) / len(scores)
            )
        else:
            average_score = 0.0

        students.append(
            {
                "average_score": average_score,
                "attendance": 0.0,
            }
        )

    # -----------------------------------------
    # 6. Calculate class analytics
    # -----------------------------------------

    analytics = calculate_class_analytics(
        students
    )

    return {
        "class_id": class_id,
        **analytics,
    }


@router.get(
    "/me/students/{student_id}/analytics",
    response_model=TeacherStudentAnalyticsResponse,
)
def get_student_analytics(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------
    # 1. Teacher authentication
    # -----------------------------------------

    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    # -----------------------------------------
    # 2. Find teacher
    # -----------------------------------------

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

    # -----------------------------------------
    # 3. Find student
    # -----------------------------------------

    student = (
        db.query(StudentProfile)
        .filter(
            StudentProfile.id == student_id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    # -----------------------------------------
    # 4. Verify teacher and student
    #    share an assigned class
    # -----------------------------------------

    shared_class = (
        db.query(ClassTeacherSubjectAssignment)
        .join(
            StudentEnrollment,
            ClassTeacherSubjectAssignment.class_id
            == StudentEnrollment.class_id,
        )
        .filter(
            ClassTeacherSubjectAssignment.teacher_id
            == teacher.id,
            StudentEnrollment.student_id
            == student.id,
            StudentEnrollment.enrollment_status
            == "ACTIVE",
        )
        .first()
    )

    if not shared_class:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this student's analytics",
        )

    # -----------------------------------------
    # 5. Get submitted assessment scores
    # -----------------------------------------

    attempts = (
        db.query(AssessmentAttempt)
        .join(
            Assessment,
            AssessmentAttempt.assessment_id
            == Assessment.id,
        )
        .filter(
            AssessmentAttempt.student_id
            == student.id,
            AssessmentAttempt.status
            == "SUBMITTED",
            Assessment.teacher_id
            == teacher.id,
        )
        .all()
    )

    scores = [
        float(attempt.score or 0)
        for attempt in attempts
    ]

    # -----------------------------------------
    # 6. Attendance
    # -----------------------------------------
    # Attendance model is not present in the
    # models we've reviewed yet.
    #
    # Therefore this is temporarily 0.0.
    # It will be connected to the actual
    # attendance system later.

    attendance = 0.0

    analytics = calculate_student_analytics(
        scores=scores,
        attendance=attendance,
    )

    return {
        "student_id": student.id,
        "student_code": student.student_id,
        "student_name": student.user.name,
        **analytics,
    }


@router.get(
    "/me/assessments/{assessment_id}/results",
    response_model=list[TeacherAssessmentResultResponse],
)
def get_assessment_results(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------
    # 1. Make sure user is a teacher
    # -----------------------------------------

    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    # -----------------------------------------
    # 2. Find teacher profile
    # -----------------------------------------

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

    # -----------------------------------------
    # 3. Make sure teacher owns assessment
    # -----------------------------------------

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id,
            Assessment.teacher_id == teacher.id,
        )
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    # -----------------------------------------
    # 4. Get student attempts
    # -----------------------------------------

    results = (
        db.query(
            AssessmentAttempt,
            StudentProfile,
            User,
        )
        .join(
            StudentProfile,
            AssessmentAttempt.student_id
            == StudentProfile.id,
        )
        .join(
            User,
            StudentProfile.user_id
            == User.id,
        )
        .filter(
            AssessmentAttempt.assessment_id
            == assessment_id,
        )
        .order_by(
            AssessmentAttempt.submitted_at.desc()
        )
        .all()
    )

    # -----------------------------------------
    # 5. Return results
    # -----------------------------------------

    return [
        TeacherAssessmentResultResponse(
            attempt_id=attempt.id,
            assessment_id=attempt.assessment_id,
            student_id=student.id,
            student_code=student.student_id,
            student_name=user.name,
            student_email=user.email,
            score=attempt.score or 0,
            max_score=assessment.max_score,
            status=attempt.status,
            submitted_at=attempt.submitted_at,
        )
        for attempt, student, user in results
    ]