from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreateUserRequestModel(BaseModel):
    prompt: str = Field(default="поиграть в настольные игры")
    group_id: Optional[list[int]] = Field(default=[37579890, 45636106])
    time_from: date = Field(default="2024-05-01")
    time_to: date = Field(default="2024-05-03")


class AddGroupsUserRequestModel(BaseModel):
    prompt: str = Field(default="поиграть в настольные игры")


class UserRequestModel(BaseModel):
    ID: int
    prompt: str
    type: int
    status: int
    group_id: Optional[list[int]] = Field(default=[])
    time_from: Optional[date]
    time_to: Optional[date]

    class Config:
        orm_mode = True


class AnswerUserRequestModel(BaseModel):
    ID: int
    prompt: str
    status: int
    tasks_count: int
    tasks_in_process: int
    tasks_done: int
    time_from: date
    time_to: date
    answer: Optional[dict] = Field(default=None)

    class Config:
        orm_mode = True


class CreateTaskModel(BaseModel):
    prompt: str
    UserRequestID: int
    type: int = Field(default=0)
    status: int = Field(default=0)
    group_id: Optional[int] = Field(default=None)
    time_from: Optional[date] = Field(default=None)
    time_to: Optional[date] = Field(default=None)

    class Config:
        orm_mode = True


class TaskModel(BaseModel):
    ID: int
    UserRequestID: int
    prompt: str
    type: int
    status: int
    group_id: Optional[int] = Field(default=None)
    time_from: Optional[date] = None
    time_to: Optional[date] = None

    class Config:
        orm_mode = True


class PostModel(BaseModel):
    ID: int
    text: str
    GroupID: int
    date: date
    vector: list[float]


class GroupModel(BaseModel):
    ID: int
    name: str
    description: str
    vector: list[float]
