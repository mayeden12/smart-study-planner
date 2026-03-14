from fastapi import FastAPI
from .api import tasks
from .database import engine, Base

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Task Manager API")

# Include the tasks router
app.include_router(tasks.router)