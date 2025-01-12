from enum import Enum
from pydantic import BaseModel


class RoleEnum(str, Enum):
    admin = "admin"
    owner = "owner"
    assistant = "assistant"


class UserBase(BaseModel):
    fullname: str
    email: str
    active: bool
    role: RoleEnum


class UserinDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True
