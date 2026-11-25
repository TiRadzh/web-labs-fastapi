from app.repositories import tasks as repository
async def list_tasks(session): return await repository.list_tasks(session)
async def find_task(session,task_id): return await repository.find_task(session,task_id)
async def create_task(session,data): return await repository.create_task(session,data)
async def update_task(session,task_id,data): return await repository.update_task(session,task_id,data)
async def delete_task(session,task_id): return await repository.delete_task(session,task_id)
async def page_tasks(session,*args): return await repository.page_tasks(session,*args)
