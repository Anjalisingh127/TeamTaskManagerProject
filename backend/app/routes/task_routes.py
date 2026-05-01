from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.project import Project
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.utils.dependencies import get_current_user, get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Create Task (Admin only)
@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only admin can create tasks
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can create tasks")

    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        due_date=task.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created", "task_id": new_task.id}


# Update Task Status (Assigned user only)
@router.put("/{task_id}")
def update_task(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only assigned user can update
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task.status = update.status
    db.commit()

    return {"message": "Task updated"}


# ✅ NEW: Get My Tasks
@router.get("/my")
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.assigned_to == current_user.id
    ).all()

    return [
    {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "project_id": task.project_id,
        "assigned_to": task.assigned_to,
        "due_date": task.due_date
    }
    for task in tasks
]