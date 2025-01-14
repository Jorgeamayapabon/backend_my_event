from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

from schemas import DatetimeSchema
from utils.enums import RoleEnum


class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    active: bool
    role: RoleEnum


class UserUpdateAdmin(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    role: Optional[RoleEnum] = None


class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase, DatetimeSchema):
    id: int
    
    class Config:
        orm_mode = True
