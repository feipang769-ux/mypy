from fastapi import APIRouter, Query, status, HTTPException
from myapi.schemas import TaskCreate, TaskRead, TaskUpdate
from myapi.db import SessionDep
from myapi.models import Task
from typing import Annotated
from sqlalchemy import select


router = APIRouter(prefix="/Task", tags=["Task"])


@router.post('', response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(session: SessionDep, payload: TaskCreate) -> Task:
    task = Task(
        title=payload.title, description=payload.description, priority=payload.priority
        )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.delete('/{task_id}', response_model=TaskRead)
async def delete_task(task_id: int, session: SessionDep) -> Task:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    #做类型效验记录，避免commit后访问已删除对象，expire_on_commit只对更新类型提交保留属性
    task_read = TaskRead.model_validate(task)  
    #delete也是一个协程
    await session.delete(task)
    await session.commit()
    return task_read


@router.patch('/{task_id}', response_model=TaskRead)
async def update_task(task_id: int, update_content: TaskUpdate, session: SessionDep) -> Task:
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = update_content.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get('/{task_id}', response_model=TaskRead)
async def seek_task(task_id: int, session: SessionDep) -> Task:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get('', response_model=list[TaskRead])
async def list_task(session: SessionDep, limit: Annotated[int, Query(le=100)] = 10) -> list[Task]:
    result = await session.execute(select(Task).limit(limit))
    return list(result.scalars().all())



