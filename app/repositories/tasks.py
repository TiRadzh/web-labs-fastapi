from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.tasks import TaskCreate

async def list_tasks(session: AsyncSession) -> list[Task]:
    result = await session.scalars(select(Task).order_by(Task.id))
    return list(result.all())

async def find_task(session: AsyncSession, task_id: int) -> Task | None:
    return await session.get(Task, task_id)

async def create_task(session: AsyncSession, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def update_task(session: AsyncSession, task_id: int, data: TaskCreate) -> Task | None:
    task = await session.get(Task, task_id)
    if task is None:
        return None
    for key, value in data.model_dump().items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(session: AsyncSession, task_id: int) -> bool:
    task = await session.get(Task, task_id)
    if task is None:
        return False
    await session.delete(task)
    await session.commit()
    return True


from sqlalchemy import func
from app.models.entities import Tag
from app.schemas.tasks import TaskRead
async def page_tasks(session,page,size,status,project_id,tag,sort_by,order,user=None):
    stmt=select(Task)
    if user is not None and user.role!="admin":
        from app.models.entities import Project
        stmt=stmt.where(Task.project.has(Project.owner_id==user.id))
    if status: stmt=stmt.where(Task.status==status)
    if project_id is not None: stmt=stmt.where(Task.project_id==project_id)
    if tag: stmt=stmt.where(Task.tags.any(Tag.name==tag))
    total=await session.scalar(select(func.count()).select_from(stmt.subquery()))
    col=getattr(Task,sort_by)
    rows=(await session.scalars(stmt.order_by(col.desc() if order=='desc' else col.asc(),Task.id).offset((page-1)*size).limit(size))).all()
    return dict(items=[TaskRead.model_validate(x) for x in rows],total=total,page=page,size=size,pages=(total+size-1)//size)
