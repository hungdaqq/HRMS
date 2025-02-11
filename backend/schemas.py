from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class CreateLeave(BaseModel):
    date: str
    reason: str


class UpdateLeave(BaseModel):
    status: str
