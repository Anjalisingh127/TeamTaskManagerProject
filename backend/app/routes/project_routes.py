from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.project import Project
from app.schemas.project_schema import ProjectCreate
from app.utils.dependencies import require_admin, get_db

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "message": "Project created successfully",
        "project_id": new_project.id
    }