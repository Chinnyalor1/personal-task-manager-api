from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    completed: bool = False
    user_id: int


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    user_id: int

    model_config = {
        "from_attributes": True
    }