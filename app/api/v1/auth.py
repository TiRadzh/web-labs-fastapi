from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from app.core.security import passwords,token,decode,get_current_user
from app.api.v1.entities import Session,save
from app.models.entities import User
from app.schemas.entities import UserRead,UserCreate
router=APIRouter()
class Credentials(UserCreate):
    password: str=Field(min_length=8,max_length=128)
class Refresh(BaseModel):
    refresh_token: str
@router.post('/auth/register',status_code=201,response_model=UserRead)
async def register(data:Credentials,s:Session):
    if await s.scalar(select(User).where(User.username==data.username)): raise HTTPException(409,'Username exists')
    return await save(s,User(username=data.username,password_hash=passwords.hash(data.password)))
def tokens(user):
    return dict(access_token=token(user,'access'),refresh_token=token(user,'refresh'),token_type='bearer')
@router.post('/auth/login')
async def login(data:Credentials,s:Session):
    user=await s.scalar(select(User).where(User.username==data.username))
    if not user or not user.password_hash or not passwords.verify(data.password,user.password_hash): raise HTTPException(401,'Invalid credentials')
    return tokens(user)
@router.post('/auth/refresh')
async def refresh(data:Refresh,s:Session):
    user=await s.get(User,decode(data.refresh_token,'refresh'))
    if not user: raise HTTPException(401,'Unknown user')
    return tokens(user)
@router.get('/users/me',response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user
@router.put('/users/me',response_model=UserRead)
async def update_me(data:UserCreate,s:Session,user=Depends(get_current_user)):
    other=await s.scalar(select(User).where(User.username==data.username,User.id!=user.id))
    if other: raise HTTPException(409,'Username exists')
    user.username=data.username
    return await save(s,user)
