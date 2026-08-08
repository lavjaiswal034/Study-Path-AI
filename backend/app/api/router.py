from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.classes import router as classes_router
from app.api.v1.student import router as student_router
from app.api.v1.teacher import router as teacher_router
from app.api.v1.prediction import router as prediction_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.roadmap import router as roadmap_router
from app.api.v1.reports import router as reports_router
from app.api.v1.notifications import router as notification_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter()


# =========================
# HEALTH
# =========================

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)


# =========================
# AUTHENTICATION
# =========================

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)


# =========================
# CLASSES
# =========================

api_router.include_router(
    classes_router,
    prefix="/classes",
    tags=["Classes"],
)

## =========================
# ADMIN
api_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"],
)

# =========================
# STUDENT
# =========================

api_router.include_router(
    student_router,
    prefix="/student",
    tags=["Student"],
)


# =========================
# TEACHER
# =========================

api_router.include_router(
    teacher_router,
    prefix="/teacher",
    tags=["Teacher"],
)


# =========================
# PREDICTION
# =========================

api_router.include_router(
    prediction_router,
    prefix="/prediction",
    tags=["Prediction"],
)


# =========================
# ANALYTICS
# =========================

api_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)


# =========================
# ROADMAP
# =========================

api_router.include_router(
    roadmap_router,
    prefix="/roadmap",
    tags=["Learning Roadmap"],
)


# =========================
# REPORTS
# =========================

api_router.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"],
)


# =========================
# NOTIFICATIONS
# =========================

api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["Notifications"],
)
