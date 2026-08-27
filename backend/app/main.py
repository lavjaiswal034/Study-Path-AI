from fastapi import FastAPI


from app.api.auth import router as auth_router
from app.core.config import settings
from app.api.students import router as students_router
from app.api.admin import router as admin_router
from app.api.enrollments import router as enrollment_router
from app.api.subjects import router as subjects_router
from app.api.assignments import router as assignments_router
from app.api.teachers import router as teachers_router
from app.api.assessments import router as assessments_router
from app.api.questions import router as questions_router
from app.api.student_assessments import (router as student_assessments_router,)
from app.api.attempts import router as attempts_router
from app.api.responses import router as responses_router
from app.api.results import router as results_router
from app.api.predictions import router as predictions_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(teachers_router)
app.include_router(enrollment_router)
app.include_router(subjects_router)
app.include_router(assignments_router)
app.include_router(assessments_router)
app.include_router(questions_router)
app.include_router(student_assessments_router)
app.include_router(attempts_router)
app.include_router(responses_router)
app.include_router(results_router)
app.include_router(predictions_router)

@app.get("/")
def root():
    return {
        "message": "StudyPath AI Backend is running",
        "version": settings.app_version,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }