from fastapi import APIRouter


router = APIRouter()


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "StudyPath AI Backend",
        "version": "1.0.0"
    }