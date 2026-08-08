from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


def build_student_report(
    student_id: int,
    student_name: str,
    analytics: dict,
    prediction: dict,
    roadmap: list[dict],
) -> dict:

    return {
        "student_id": student_id,
        "student_name": student_name,
        "generated_at": datetime.utcnow().isoformat(),
        "analytics": analytics,
        "prediction": prediction,
        "roadmap": roadmap,
    }


def generate_student_pdf(report: dict) -> BytesIO:

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "StudyPath AI - Student Performance Report",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Student:</b> {report['student_name']}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Student ID:</b> {report['student_id']}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {report['generated_at']}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 20))

    # Performance Analytics

    story.append(
        Paragraph(
            "Performance Analytics",
            styles["Heading2"],
        )
    )

    analytics = report["analytics"]

    analytics_data = [
        ["Metric", "Value"],
        [
            "Average Score",
            str(analytics.get("average_score", "N/A")),
        ],
        [
            "Highest Score",
            str(analytics.get("highest_score", "N/A")),
        ],
        [
            "Lowest Score",
            str(analytics.get("lowest_score", "N/A")),
        ],
        [
            "Attendance",
            str(analytics.get("attendance", "N/A")),
        ],
        [
            "Performance Level",
            str(
                analytics.get(
                    "performance_level",
                    "N/A",
                )
            ),
        ],
        [
            "Total Assessments",
            str(
                analytics.get(
                    "total_assessments",
                    "N/A",
                )
            ),
        ],
    ]

    table = Table(
        analytics_data,
        colWidths=[220, 220],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # ML Prediction

    story.append(
        Paragraph(
            "ML Prediction",
            styles["Heading2"],
        )
    )

    prediction = report["prediction"]

    prediction_data = [
        ["Prediction Metric", "Value"],
        [
            "Predicted Score",
            str(
                prediction.get(
                    "predicted_score",
                    "N/A",
                )
            ),
        ],
        [
            "Risk Level",
            str(
                prediction.get(
                    "risk_level",
                    "N/A",
                )
            ),
        ],
        [
            "Confidence",
            str(
                prediction.get(
                    "confidence",
                    "N/A",
                )
            ),
        ],
    ]

    prediction_table = Table(
        prediction_data,
        colWidths=[220, 220],
    )

    prediction_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(prediction_table)

    story.append(Spacer(1, 20))

    # Learning Roadmap

    story.append(
        Paragraph(
            "Personalized Learning Roadmap",
            styles["Heading2"],
        )
    )

    for index, item in enumerate(
        report["roadmap"],
        start=1,
    ):

        story.append(
            Paragraph(
                f"<b>{index}. "
                f"{item.get('topic', 'Topic')}</b>",
                styles["Heading3"],
            )
        )

        story.append(
            Paragraph(
                f"Priority: "
                f"{item.get('priority', 'N/A')}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Estimated Hours: "
                f"{item.get('estimated_hours', 'N/A')}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                item.get("description", ""),
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 10))

    document.build(story)

    buffer.seek(0)

    return buffer