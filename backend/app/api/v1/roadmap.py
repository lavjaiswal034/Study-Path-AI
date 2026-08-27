from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.roles import require_role

from app.models.roadmap import Roadmap
from app.models.roadmap_task import RoadmapTask
from app.models.task_progress import StudentTaskProgress

from app.schemas.roadmap import (
    RoadmapRequest,
    RoadmapResponse,
)

from app.services.analytics_service import detect_weak_areas
from app.services.roadmap_service import (
    create_personalized_roadmap,
)


router = APIRouter()


# =========================================================
# ROADMAP STATUS
# =========================================================

@router.get("/status")
def roadmap_status():
    return {
        "message": "Learning roadmap module is working"
    }


# =========================================================
# GET TASK PROGRESS
# =========================================================

@router.get(
    "/tasks/{task_id}/progress",
)
def get_task_progress(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    student_id = current_user["user_id"]

    task = (
        db.query(RoadmapTask)
        .join(
            Roadmap,
            RoadmapTask.roadmap_id == Roadmap.id,
        )
        .filter(
            RoadmapTask.id == task_id,
            Roadmap.student_id == student_id,
            Roadmap.status == "ACTIVE",
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Roadmap task not found",
        )

    progress = (
        db.query(StudentTaskProgress)
        .filter(
            StudentTaskProgress.student_id == student_id,
            StudentTaskProgress.task_id == task_id,
        )
        .first()
    )

    if not progress:
        return {
            "task_id": task_id,
            "status": "PENDING",
            "started_at": None,
            "completed_at": None,
        }

    return {
        "task_id": task_id,
        "status": progress.status,
        "started_at": progress.started_at,
        "completed_at": progress.completed_at,
    }
# =========================================================
# GENERATE ROADMAP
# =========================================================

@router.post(
    "/generate",
    response_model=RoadmapResponse,
)
async def generate_roadmap(
    request: RoadmapRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    # -----------------------------------------
    # 1. Make sure student is generating
    #    their own roadmap
    # -----------------------------------------

    if request.student_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only generate a roadmap for yourself",
        )

    # -----------------------------------------
    # 2. Temporary topic scores
    # -----------------------------------------
    # Later these will come from actual
    # assessment/student performance data.

    topic_scores = {
        "Python": 72,
        "SQL": 45,
        "Data Structures": 38,
        "Machine Learning": 67,
        "Statistics": 42,
    }

    weak_areas = detect_weak_areas(
        topic_scores=topic_scores,
        threshold=50,
    )

    weak_topics = [
        area["topic"]
        for area in weak_areas
    ]

    # -----------------------------------------
    # 3. Generate personalized roadmap
    # -----------------------------------------

    result = await create_personalized_roadmap(
        student_id=request.student_id,
        predicted_score=request.predicted_score,
        risk_level=request.risk_level,
        weak_topics=weak_topics,
        study_hours_per_day=request.study_hours_per_day,
    )

    if result.get("success") is False:
        raise HTTPException(
            status_code=503,
            detail="LLM service is currently unavailable",
        )

    roadmap_items = result.get(
        "roadmap",
        [],
    )

    # -----------------------------------------
    # 4. Create Roadmap database record
    # -----------------------------------------
    # -----------------------------------------
# 4. Archive previous active roadmap
# -----------------------------------------

    existing_roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.student_id == request.student_id,
            Roadmap.status == "ACTIVE",
        )
        .all()
    )

    for old_roadmap in existing_roadmap:
        old_roadmap.status = "ARCHIVED"
    roadmap = Roadmap(
        student_id=request.student_id,
        title="Personalized Learning Roadmap",
        description=(
            "Personalized learning roadmap "
            "generated based on student performance."
        ),
        status="ACTIVE",
    )

    db.add(roadmap)
    db.flush()

    # -----------------------------------------
    # 5. Create RoadmapTask records
    # -----------------------------------------

    for item in roadmap_items:

        task = RoadmapTask(
            roadmap_id=roadmap.id,
            title=item.get(
                "topic",
                "Learning Task",
            ),
            description=item.get(
                "description",
                "",
            ),
            task_type="STUDY",
            priority=item.get(
                "priority",
                "MEDIUM",
            ).upper(),
            status="PENDING",
            estimated_hours=item.get(
                "estimated_hours",
                0.0,
            ),
        )

        db.add(task)

    # -----------------------------------------
    # 6. Save everything
    # -----------------------------------------

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save roadmap",
        )


    # -----------------------------------------
    # 7. Return roadmap to frontend
    # -----------------------------------------

    return {
        "student_id": request.student_id,
        "roadmap": roadmap_items,
        "message": result.get(
            "message",
            "Learning roadmap generated successfully",
        ),
    }

# =========================================================
# ROADMAP PROGRESS
# =========================================================

@router.get(
    "/progress",
)
def get_roadmap_progress(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    student_id = current_user["user_id"]

    roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.student_id == student_id,
            Roadmap.status == "ACTIVE",
        )
        .order_by(
            Roadmap.created_at.desc()
        )
        .first()
    )

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="No active roadmap found",
        )

    tasks = (
        db.query(RoadmapTask)
        .filter(
            RoadmapTask.roadmap_id == roadmap.id
        )
        .all()
    )

    total_tasks = len(tasks)

    completed_tasks = sum(
        1
        for task in tasks
        if task.status == "COMPLETED"
    )

    in_progress_tasks = sum(
        1
        for task in tasks
        if task.status == "IN_PROGRESS"
    )

    pending_tasks = sum(
        1
        for task in tasks
        if task.status == "PENDING"
    )

    if total_tasks == 0:
        completion_percentage = 0.0
    else:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100,
            2,
        )

    return {
        "roadmap_id": roadmap.id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage,
    }

# =========================================================
# GET MY ACTIVE ROADMAP
# =========================================================

@router.get("/")
def get_my_roadmap(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    student_id = current_user["user_id"]

    roadmap = (
        db.query(Roadmap)
        .filter(
            Roadmap.student_id == student_id,
            Roadmap.status == "ACTIVE",
        )
        .order_by(
            Roadmap.created_at.desc()
        )
        .first()
    )

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="No active roadmap found",
        )

    tasks = (
        db.query(RoadmapTask)
        .filter(
            RoadmapTask.roadmap_id == roadmap.id
        )
        .order_by(
            RoadmapTask.id.asc()
        )
        .all()
    )

    return {
        "roadmap_id": roadmap.id,
        "student_id": roadmap.student_id,
        "title": roadmap.title,
        "description": roadmap.description,
        "status": roadmap.status,
        "created_at": roadmap.created_at,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "task_type": task.task_type,
                "priority": task.priority,
                "status": task.status,
                "estimated_hours": task.estimated_hours,
                "due_date": task.due_date,
            }
            for task in tasks
        ],
    }


# =========================================================
# START TASK
# =========================================================

@router.post(
    "/tasks/{task_id}/start",
)
def start_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    student_id = current_user["user_id"]

    task = (
        db.query(RoadmapTask)
        .join(
            Roadmap,
            RoadmapTask.roadmap_id == Roadmap.id,
        )
        .filter(
            RoadmapTask.id == task_id,
            Roadmap.student_id == student_id,
            Roadmap.status == "ACTIVE",
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Roadmap task not found",
        )

    progress = (
        db.query(StudentTaskProgress)
        .filter(
            StudentTaskProgress.student_id == student_id,
            StudentTaskProgress.task_id == task_id,
        )
        .first()
    )

    if progress:

        if progress.status == "COMPLETED":
            raise HTTPException(
                status_code=400,
                detail="Task is already completed",
            )

        return {
            "message": "Task already started",
            "task_id": task_id,
            "status": progress.status,
        }

    progress = StudentTaskProgress(
        student_id=student_id,
        task_id=task_id,
        status="IN_PROGRESS",
        started_at=datetime.utcnow(),
    )

    db.add(progress)

    task.status = "IN_PROGRESS"

    db.commit()
    db.refresh(progress)

    return {
        "message": "Task started successfully",
        "task_id": task_id,
        "status": progress.status,
        "started_at": progress.started_at,
    }


# =========================================================
# COMPLETE TASK
# =========================================================

@router.post(
    "/tasks/{task_id}/complete",
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("student")
    ),
):

    student_id = current_user["user_id"]

    task = (
        db.query(RoadmapTask)
        .join(
            Roadmap,
            RoadmapTask.roadmap_id == Roadmap.id,
        )
        .filter(
            RoadmapTask.id == task_id,
            Roadmap.student_id == student_id,
            Roadmap.status == "ACTIVE",
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Roadmap task not found",
        )

    progress = (
        db.query(StudentTaskProgress)
        .filter(
            StudentTaskProgress.student_id == student_id,
            StudentTaskProgress.task_id == task_id,
        )
        .first()
    )

    if not progress:

        now = datetime.utcnow()

        progress = StudentTaskProgress(
            student_id=student_id,
            task_id=task_id,
            status="COMPLETED",
            started_at=now,
            completed_at=now,
        )

        db.add(progress)

    else:

        if progress.status == "COMPLETED":
            raise HTTPException(
                status_code=400,
                detail="Task is already completed",
            )

        progress.status = "COMPLETED"

        if progress.started_at is None:
            progress.started_at = datetime.utcnow()

        progress.completed_at = datetime.utcnow()

    task.status = "COMPLETED"

    db.commit()
    db.refresh(progress)

    return {
        "message": "Task completed successfully",
        "task_id": task_id,
        "status": progress.status,
        "completed_at": progress.completed_at,
    }