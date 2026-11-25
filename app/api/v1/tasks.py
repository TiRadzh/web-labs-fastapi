from app.core.security import get_current_user
from app.api.v1.entities import check_task, check_owner, find
from app.models.entities import Project
from fastapi import Query
from typing import Literal
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.tasks import TaskCreate, TaskRead
from app.services import tasks as service

router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)])
Session = Annotated[AsyncSession, Depends(get_session)]

@router.get("")
async def get_tasks(session: Session, user=Depends(get_current_user), page: int=Query(1,ge=1), size: int=Query(10,ge=1,le=100), status: str|None=None, project_id: int|None=None, tag: str|None=None, sort_by: Literal['id','created_at','title']='id', order: Literal['asc','desc']='asc'):
    return await service.page_tasks(session,page,size,status,project_id,tag,sort_by,order,user)

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, session: Session, user=Depends(get_current_user)):
    await check_task(session,task_id,user)
    task = await service.find_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, session: Session):
    raise HTTPException(403, "Create tasks through a project")

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, data: TaskCreate, session: Session, user=Depends(get_current_user)):
    await check_task(session,task_id,user)
    task = await service.update_task(session, task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: Session, user=Depends(get_current_user)):
    await check_task(session,task_id,user)
    if not await service.delete_task(session, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
