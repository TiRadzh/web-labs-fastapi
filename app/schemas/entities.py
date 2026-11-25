from pydantic import BaseModel, Field, ConfigDict
class UserCreate(BaseModel):
    username: str = Field(min_length=1,max_length=100)
class UserRead(UserCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
class ProjectCreate(BaseModel):
    title: str = Field(min_length=1,max_length=200)
    owner_id: int | None = None
class ProjectRead(ProjectCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
class CommentCreate(BaseModel):
    text: str = Field(min_length=1,max_length=2000)
    user_id: int | None = None
class CommentRead(CommentCreate):
    id: int
    task_id: int
    model_config = ConfigDict(from_attributes=True)
