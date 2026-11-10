from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class TaskCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = None
    priority: Literal['low', 'medium', 'high'] | None = None


class TaskRead(BaseModel):
#sqlalchemy -> pydantic, 把orm的属性按字段名读进模型而不只是dict输入
    model_config = ConfigDict(from_attributes=True)   

    id: int
    title: str
    description: str | None = None
    status: Literal['pending', 'achieved', 'cancelled']
    priority: Literal['low', 'medium', 'high'] | None = None
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    status: Literal['pending', 'achieved', 'cancelled'] | None = None
    priority: Literal['low', 'medium', 'high'] | None = None

