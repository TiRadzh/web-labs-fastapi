from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy import select, func
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.entities import User, Project, Comment, Tag
from app.models.task import Task
from app.schemas.entities import UserCreate, UserRead, ProjectCreate, ProjectRead, CommentCreate, CommentRead
from app.schemas.tasks import TaskCreate, TaskRead
router = APIRouter()
Session = Annotated[AsyncSession, Depends(get_session)]
async def find(s, model, id):
    obj = await s.get(model,id)
    if obj is None: raise HTTPException(404,'Not found')
    return obj
async def save(s,obj):
    s.add(obj)
    await s.commit()
    await s.refresh(obj)
    return obj
@router.post('/users',response_model=UserRead,status_code=201)
async def user(data: UserCreate,s: Session):
    if await s.scalar(select(User).where(User.username==data.username)): raise HTTPException(409,'Username exists')
    return await save(s,User(**data.model_dump()))
@router.post('/projects',response_model=ProjectRead,status_code=201)
async def create_project(data: ProjectCreate,s: Session):
    await find(s,User,data.owner_id)
    return await save(s,Project(**data.model_dump()))
@router.get('/projects')
async def projects(s: Session,page: int=Query(1,ge=1),size: int=Query(10,ge=1,le=100)):
    total=await s.scalar(select(func.count()).select_from(Project))
    items=(await s.scalars(select(Project).order_by(Project.id).offset((page-1)*size).limit(size))).all()
    return dict(items=[ProjectRead.model_validate(x) for x in items],total=total,page=page,size=size,pages=(total+size-1)//size)
@router.get('/projects/{project_id}',response_model=ProjectRead)
async def project(project_id:int,s:Session):
    return await find(s,Project,project_id)
@router.put('/projects/{project_id}',response_model=ProjectRead)
async def update_project(project_id:int,data:ProjectCreate,s:Session):
    obj=await find(s,Project,project_id)
    await find(s,User,data.owner_id)
    obj.title=data.title
    obj.owner_id=data.owner_id
    return await save(s,obj)
@router.delete('/projects/{project_id}',status_code=204)
async def delete_project(project_id:int,s:Session):
    await s.delete(await find(s,Project,project_id)); await s.commit()
    return Response(status_code=204)
@router.post('/projects/{project_id}/tasks',response_model=TaskRead,status_code=201)
async def project_task(project_id:int,data:TaskCreate,s:Session):
    await find(s,Project,project_id)
    return await save(s,Task(**data.model_dump(),project_id=project_id))
@router.post('/tasks/{task_id}/comments',response_model=CommentRead,status_code=201)
async def comment(task_id:int,data:CommentCreate,s:Session):
    await find(s,Task,task_id); await find(s,User,data.user_id)
    return await save(s,Comment(**data.model_dump(),task_id=task_id))
@router.get('/tasks/{task_id}/comments',response_model=list[CommentRead])
async def comments(task_id:int,s:Session):
    await find(s,Task,task_id)
    return (await s.scalars(select(Comment).where(Comment.task_id==task_id).limit(100))).all()
@router.post('/tasks/{task_id}/tags/{name}',status_code=201)
async def tag(task_id:int,name:str,s:Session):
    task=await find(s,Task,task_id)
    obj=await s.scalar(select(Tag).where(Tag.name==name))
    if obj is None: obj=Tag(name=name)
    if obj not in task.tags: task.tags.append(obj)
    await s.commit()
    return {'name':name}
