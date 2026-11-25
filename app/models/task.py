from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.models.entities import task_tags
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), server_default='todo')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    project_id: Mapped[int | None] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    project = relationship('Project', back_populates='tasks')
    tags = relationship('Tag', secondary=task_tags, lazy='selectin')
    comments = relationship('Comment', cascade='all, delete-orphan')
