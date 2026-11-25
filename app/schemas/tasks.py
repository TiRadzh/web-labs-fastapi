from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: Literal["todo", "in_progress", "done", "archived"] = "todo"
    description: str | None = None


class TaskRead(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
