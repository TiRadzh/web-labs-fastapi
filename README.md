# Task Manager API — lab-04-relations
Python 3.11, FastAPI, SQLAlchemy, Alembic.

```powershell
python -m pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

Тесты: `python -m pytest`. DATABASE_URL задаёт адрес БД (по умолчанию SQLite). APP_SECRET_KEY — секрет JWT, UPLOAD_DIR — папка вложений. Для существующей БД ЛР2 без alembic_version сначала сделайте резервную копию и выполните `alembic stamp 0001`, только если схема соответствует ЛР2.

Учебная версия: используйте отдельную БД для каждой ветки либо применяйте миграции последовательно. Перед откатом сохраните резервную копию.
