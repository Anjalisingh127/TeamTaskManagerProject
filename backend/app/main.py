from fastapi import FastAPI, Depends # Added Depends
from sqlalchemy.orm import Session # Added Session
from typing import List # Added List
from .database import Base, engine, get_db # Added get_db
from .models import user, project, task
from . import models, schemas, auth, database # Added these for the new route
from .routes import auth_routes, test_routes, project_routes, task_routes, dashboard_routes

app = FastAPI(title="Team Task Manager API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(auth_routes.router)
app.include_router(test_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(dashboard_routes.router)

@app.get("/")
def home():
    return {"message": "API is running successfully"}

# ✅ This route is now fully functional with correct imports
@app.get("/tasks", response_model=List[schemas.TaskOut], tags=["Tasks"])
def get_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    # Members see only their tasks; Admins see everything
    if current_user.role == "admin":
        return db.query(models.Task).all()
    return db.query(models.Task).filter(models.Task.assigned_to == current_user.id).all()