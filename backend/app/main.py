from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, project, task
from app.routes import auth_routes, test_routes
from app.routes import project_routes
from app.routes import task_routes
from app.routes import dashboard_routes

app = FastAPI(title="Team Task Manager API")

Base.metadata.create_all(bind=engine)

# ✅ Register routes AFTER app is created
app.include_router(auth_routes.router)
app.include_router(test_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(dashboard_routes.router)

@app.get("/")
def home():
    return {"message": "API is running successfully"}