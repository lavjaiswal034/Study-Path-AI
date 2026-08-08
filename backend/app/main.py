from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(
    title="StudyPath AI Backend",
    description="Backend API for Student Performance Prediction and Personalized Learning Path Recommendation",
    version="1.0.0",
)


app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to StudyPath AI Backend 🚀"
    }