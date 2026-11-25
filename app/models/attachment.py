from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
class Attachment(Base):
    __tablename__='attachments'
    id: Mapped[int]=mapped_column(primary_key=True)
    filename: Mapped[str]=mapped_column(String(255))
    file_path: Mapped[str]=mapped_column(String(255))
    content_type: Mapped[str]=mapped_column(String(100))
    size: Mapped[int]
    task_id: Mapped[int]=mapped_column(ForeignKey('tasks.id',ondelete='CASCADE'))
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime]=mapped_column(server_default=func.now())
