from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    salary: int
    title: str
    full_name: str
    profile_image: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    title: Optional[str] = None
    salary: Optional[str] = None
    profile_image: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class CreateLeave(BaseModel):
    date: str
    reason: str


class UpdateLeave(BaseModel):
    status: str


class CreateAttendance(BaseModel):
    username: str
    date: str
    status: str
