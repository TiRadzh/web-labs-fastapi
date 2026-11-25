from app.core.config import settings
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.db.session import get_session
from app.models.entities import User
passwords=PasswordHash.recommended()
secret=settings.app_secret_key
bearer=HTTPBearer(auto_error=False)
def token(user,kind):
    return jwt.encode({'sub':str(user.id),'kind':kind,'exp':datetime.now(timezone.utc)+timedelta(minutes=30 if kind=='access' else 10080)},secret,algorithm='HS256')
def decode(value,kind):
    try:
        data=jwt.decode(value,secret,algorithms=['HS256'],options={'require':['exp','sub','kind']})
        if data['kind']!=kind: raise ValueError()
        return int(data['sub'])
    except (jwt.PyJWTError,ValueError,KeyError): raise HTTPException(401,'Invalid token')
async def get_current_user(credentials=Depends(bearer),s=Depends(get_session)):
    if credentials is None: raise HTTPException(401,'Authentication required')
    user=await s.get(User,decode(credentials.credentials,'access'))
    if user is None: raise HTTPException(401,'Unknown user')
    return user
