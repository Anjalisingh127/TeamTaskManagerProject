from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.task import Task
from app.utils.dependencies import get_current_user, get_db
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total_tasks = db.query(Task).count()

    completed_tasks = db.query(Task).filter(
        Task.status == "DONE"
    ).count()

    pending_tasks = db.query(Task).filter(
        Task.status != "DONE"
    ).count()

    my_tasks = db.query(Task).filter(
        Task.assigned_to == current_user.id
    ).count()

    # ✅ NEW: Overdue Tasks
    overdue_tasks = db.query(Task).filter(
        Task.due_date != None,  # ensure due_date exists
        Task.due_date < datetime.utcnow(),
        Task.status != "DONE"
    ).count()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,  # ✅ added
        "my_tasks": my_tasks
    }