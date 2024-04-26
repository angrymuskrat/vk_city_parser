from datetime import datetime

from pydantic import BaseModel


class UserRequestModel(BaseModel):
    ID: int
    prompt: str
    type: int
    status: int
    # group_id: int
    time_from: datetime
    time_to: datetime

    class Config:
        orm_mode = True


class TaskModel(BaseModel):
    ID: int
    prompt: str
    type: int
    # group_id: int
    time_from: datetime
    time_to: datetime


class PostModel(BaseModel):
    ID: int
    text: str
    GroupID: int
    vector: float


class GroupModel(BaseModel):
    ID: int
    description: str
    vector: float
