from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.roles import require_role
from app.schemas.reports import (
    ReportRequest,
    ReportResponse,
)
from app.services.report_service import (
    build_student_report,
    generate_student_pdf,
)


router = APIRouter()


@router.get("/status")
def reports_status():
    return {
        "message": "Reports module is working"
    }


@router.post(
    "/student",
    response_model=ReportResponse,
)
def generate_student_report(
    request: ReportRequest,
    current_user: dict = Depends(
        require_role("student")
    ),
):
    if request.student_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only generate a report for yourself",
        )

    analytics = {
        "average_score": 72.0,
        "highest_score": 85.0,
        "lowest_score": 58.0,
        "attendance": 85.0,
        "performance_level": "good",
        "total_assessments": 5,
    }

    prediction = {
        "predicted_score": 78.5,
        "risk_level": "low",
        "confidence": 0.80,
    }

    roadmap = [
        {
            "topic": "SQL",
            "priority": "high",
            "estimated_hours": 6,
            "description": (
                "Improve SQL fundamentals "
                "and query practice."
            ),
            "resources": [
                "SQL fundamentals",
                "Practice SQL queries",
            ],
        },
        {
            "topic": "Data Structures",
            "priority": "medium",
            "estimated_hours": 8,
            "description": (
                "Practice arrays, linked lists "
                "and trees."
            ),
            "resources": [
                "Data structures concepts",
                "Coding practice",
            ],
        },
    ]

    report = build_student_report(
        student_id=current_user["user_id"],
        student_name=current_user.get(
            "name",
            "Student",
        ),
        analytics=analytics,
        prediction=prediction,
        roadmap=roadmap,
    )

    return report


@router.post("/student/pdf")
def generate_student_pdf_report(
    request: ReportRequest,
    current_user: dict = Depends(
        require_role("student")
    ),
):
    if request.student_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only generate a report for yourself",
        )

    analytics = {
        "average_score": 72.0,
        "highest_score": 85.0,
        "lowest_score": 58.0,
        "attendance": 85.0,
        "performance_level": "good",
        "total_assessments": 5,
    }

    prediction = {
        "predicted_score": 78.5,
        "risk_level": "low",
        "confidence": 0.80,
    }

    roadmap = [
        {
            "topic": "SQL",
            "priority": "high",
            "estimated_hours": 6,
            "description": (
                "Improve SQL fundamentals "
                "and query practice."
            ),
            "resources": [
                "SQL fundamentals",
                "Practice SQL queries",
            ],
        },
        {
            "topic": "Data Structures",
            "priority": "medium",
            "estimated_hours": 8,
            "description": (
                "Practice arrays, linked lists "
                "and trees."
            ),
            "resources": [
                "Data structures concepts",
                "Coding practice",
            ],
        },
    ]

    report = build_student_report(
        student_id=current_user["user_id"],
        student_name=current_user.get(
            "name",
            "Student",
        ),
        analytics=analytics,
        prediction=prediction,
        roadmap=roadmap,
    )

    pdf = generate_student_pdf(report)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="student_report.pdf"'
            )
        },
    )