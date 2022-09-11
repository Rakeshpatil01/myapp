from typing import List, Union
from datetime import date
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    username: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    email: str
    password: str
    username: str

    class Config:
        orm_mode = True


class history_Data(BaseModel):
    symbol: str
    interval: str
    start_date: date
    end_date: date
