import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_session
@pytest.fixture
def client(tmp_path,monkeypatch):
    import app.api.v1.attachments as attachments
    monkeypatch.setattr(attachments,'folder',tmp_path/'uploads')
    engine=create_async_engine('sqlite+aiosqlite:///'+str(tmp_path/'test.db'))
    async def setup():
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    asyncio.run(setup())
    factory=async_sessionmaker(engine,expire_on_commit=False)
    async def session():
        async with factory() as s: yield s
    app.dependency_overrides[get_session]=session
    with TestClient(app) as c: yield c
    app.dependency_overrides.clear(); asyncio.run(engine.dispose())
@pytest.fixture
def auth(client):
    data={'username':'student','password':'password123'}
    user=client.post('/api/v1/auth/register',json=data).json()
    token=client.post('/api/v1/auth/login',json=data).json()['access_token']
    client.headers['Authorization']='Bearer '+token
    return user
@pytest.fixture
def project(client,auth):
    return client.post('/api/v1/projects',json={'title':'Project','owner_id':auth['id']}).json()['id']
@pytest.fixture
def task(client,project):
    return client.post(f'/api/v1/projects/{project}/tasks',json={'title':'Task'}).json()['id']
