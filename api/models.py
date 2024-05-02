from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreateUserRequestModel(BaseModel):
    prompt: str = Field(default="поиграть в настольные игры")
    group_id: Optional[int] = Field(default=45636106)
    time_from: date = Field(default="2024-03-01")
    time_to: date = Field(default="2024-03-31")


class UserRequestModel(BaseModel):
    ID: int
    prompt: str
    type: int
    status: int
    group_id: Optional[int] = Field(default=None)
    time_from: date
    time_to: date

    class Config:
        orm_mode = True


class CreateTaskModel(BaseModel):
    prompt: str
    UserRequestID: int
    type: int
    group_id: Optional[int] = Field(default=None)
    time_from: date
    time_to: date


class TaskModel(BaseModel):
    ID: int
    prompt: str
    UserRequestID: int
    type: int
    group_id: Optional[int] = Field(default=None)
    time_from: date
    time_to: date


class PostModel(BaseModel):
    ID: int
    text: str
    GroupID: int
    date: date
    vector: list[float]


class GroupModel(BaseModel):
    ID: int
    description: str
    vector: list[float]
