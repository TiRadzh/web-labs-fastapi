from fastapi import FastAPI
from app.api.v1.tasks import router as tasks_router
app = FastAPI(title='Task Manager API', version='7.0.0')
app.include_router(tasks_router, prefix='/api/v1')

from app.api.v1.entities import router as entities_router
app.include_router(entities_router,prefix="/api/v1")
from app.api.v1.auth import router as auth_router
app.include_router(auth_router,prefix="/api/v1")
from app.api.v1.attachments import router as attachments_router
app.include_router(attachments_router,prefix="/api/v1")