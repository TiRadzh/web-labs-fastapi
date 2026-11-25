import os, logging
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy import select
from app.api.v1.entities import Session,check_task,find,save
from app.core.security import get_current_user
from app.models.attachment import Attachment
router=APIRouter()
folder=Path(os.getenv('UPLOAD_DIR','uploads'))
allowed={'.txt':'text/plain','.pdf':'application/pdf','.png':'image/png','.jpg':'image/jpeg'}
def metadata(obj):
    return {k:getattr(obj,k) for k in ('id','filename','content_type','size','task_id','user_id','created_at')}
@router.post('/tasks/{task_id}/attachments',status_code=201)
async def upload(task_id:int,file:UploadFile,background:BackgroundTasks,s:Session,user=Depends(get_current_user)):
    await check_task(s,task_id,user)
    name=Path((file.filename or '').replace('\\','/')).name
    ext=Path(name).suffix.lower()
    if ext not in allowed or file.content_type!=allowed[ext]: raise HTTPException(415,'Unsupported file type')
    data=await file.read(5*1024*1024+1)
    if len(data)>5*1024*1024: raise HTTPException(413,'File too large')
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/(uuid4().hex+ext)
    path.write_bytes(data)
    try: obj=await save(s,Attachment(filename=name,file_path=str(path),content_type=file.content_type,size=len(data),task_id=task_id,user_id=user.id))
    except Exception:
        path.unlink(missing_ok=True); raise
    background.add_task(logging.getLogger(__name__).warning,'Attachment uploaded: %s',obj.id)
    return metadata(obj)
@router.get('/tasks/{task_id}/attachments')
async def attachments(task_id:int,s:Session,user=Depends(get_current_user)):
    await check_task(s,task_id,user)
    return [metadata(x) for x in (await s.scalars(select(Attachment).where(Attachment.task_id==task_id).limit(100))).all()]
@router.get('/attachments/{attachment_id}')
async def download(attachment_id:int,s:Session,user=Depends(get_current_user)):
    obj=await find(s,Attachment,attachment_id); await check_task(s,obj.task_id,user)
    return FileResponse(obj.file_path,filename=obj.filename,media_type='application/octet-stream')
@router.delete('/attachments/{attachment_id}',status_code=204)
async def delete(attachment_id:int,s:Session,user=Depends(get_current_user)):
    obj=await find(s,Attachment,attachment_id); await check_task(s,obj.task_id,user)
    path=Path(obj.file_path); await s.delete(obj); await s.commit(); path.unlink(missing_ok=True)
    return Response(status_code=204)
