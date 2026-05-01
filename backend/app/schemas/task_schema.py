from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assigned_to: int
    due_date: datetime


class TaskUpdate(BaseModel):
    status: str