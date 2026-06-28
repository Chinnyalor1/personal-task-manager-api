from fastapi import FastAPI
import logging

from app.database import engine
from app.models import Base
from app.routes.task_routes import router as task_router
from app.routes.auth_routes import router as auth_router

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
