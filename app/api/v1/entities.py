from app.core.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy import select, func
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.entities import User, Project, Comment, Tag
from app.models.task import Task
from app.schemas.entities import UserCreate, UserRead, ProjectCreate, ProjectRead, CommentCreate, CommentRead
from app.schemas.tasks import TaskCreate, TaskRead
router = APIRouter(dependencies=[Depends(get_current_user)])
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
@router.post('/projects',response_model=ProjectRead,status_code=201)
async def create_project(data: ProjectCreate,s: Session,user=Depends(get_current_user)):
    return await save(s,Project(title=data.title,owner_id=user.id))
@router.get('/projects')
async def projects(s: Session,user=Depends(get_current_user),page: int=Query(1,ge=1),size: int=Query(10,ge=1,le=100)):
    stmt=select(Project)
    if user.role!="admin": stmt=stmt.where(Project.owner_id==user.id)
    total=await s.scalar(select(func.count()).select_from(stmt.subquery()))
    items=(await s.scalars(stmt.order_by(Project.id).offset((page-1)*size).limit(size))).all()
    return dict(items=[ProjectRead.model_validate(x) for x in items],total=total,page=page,size=size,pages=(total+size-1)//size)
@router.get('/projects/{project_id}',response_model=ProjectRead)
async def project(project_id:int,s:Session,user=Depends(get_current_user)):
    obj=await find(s,Project,project_id); check_owner(obj,user)
    return obj
@router.put('/projects/{project_id}',response_model=ProjectRead)
async def update_project(project_id:int,data:ProjectCreate,s:Session,user=Depends(get_current_user)):
    obj=await find(s,Project,project_id)
    check_owner(obj,user)
    obj.title=data.title
    return await save(s,obj)
@router.delete('/projects/{project_id}',status_code=204)
async def delete_project(project_id:int,s:Session,user=Depends(get_current_user)):
    obj=await find(s,Project,project_id); check_owner(obj,user)
    await s.delete(obj); await s.commit()
    return Response(status_code=204)
@router.post('/projects/{project_id}/tasks',response_model=TaskRead,status_code=201)
async def project_task(project_id:int,data:TaskCreate,s:Session,user=Depends(get_current_user)):
    check_owner(await find(s,Project,project_id),user)
    return await save(s,Task(**data.model_dump(),project_id=project_id))
@router.post('/tasks/{task_id}/comments',response_model=CommentRead,status_code=201)
async def comment(task_id:int,data:CommentCreate,s:Session,user=Depends(get_current_user)):
    await check_task(s,task_id,user)
    return await save(s,Comment(text=data.text,user_id=user.id,task_id=task_id))
@router.get('/tasks/{task_id}/comments',response_model=list[CommentRead])
async def comments(task_id:int,s:Session,user=Depends(get_current_user)):
    await check_task(s,task_id,user)
    return (await s.scalars(select(Comment).where(Comment.task_id==task_id).limit(100))).all()
@router.post('/tasks/{task_id}/tags/{name}',status_code=201)
async def tag(task_id:int,name:str,s:Session,user=Depends(get_current_user)):
    task=await check_task(s,task_id,user)
    obj=await s.scalar(select(Tag).where(Tag.name==name))
    if obj is None: obj=Tag(name=name)
    if obj not in task.tags: task.tags.append(obj)
    await s.commit()
    return {'name':name}

def check_owner(project,user):
    if user.role!='admin' and project.owner_id!=user.id: raise HTTPException(403,'Forbidden')
async def check_task(s,id,user):
    task=await find(s,Task,id)
    if task.project_id is None:
        if user.role!='admin': raise HTTPException(403,'Forbidden')
    else: check_owner(await find(s,Project,task.project_id),user)
    return task
