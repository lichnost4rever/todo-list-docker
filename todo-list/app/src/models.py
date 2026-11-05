from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: int = Field(1, ge=1, le=5)
    due_date: Optional[date] = None
    done: bool = False


class TaskCreate(TaskBase):
    """Схема для POST — без id."""
    pass


class TaskUpdate(BaseModel):
    """Все поля опциональны для PUT."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[date] = None
    done: Optional[bool] = None


class Task(TaskBase):
    """Схема ответа — с id."""
    id: int