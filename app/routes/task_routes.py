from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.models import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info("Creating a new task")

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        completed=task.completed,
        user_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info("Task created successfully")

    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@router.get("/tasks/search")
def search_tasks(keyword: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(
        Task.title.ilike(f"%{keyword}%")
    ).all()

    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        logger.info("Task not found")
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        logger.info("Task not found")
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority

    db.commit()
    db.refresh(task)

    logger.info("Task updated successfully")

    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        logger.info("Task not found")
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    logger.info("Task deleted successfully")

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        logger.info("Task not found")
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True

    db.commit()
    db.refresh(task)

    logger.info("Task marked complete successfully")

    return task