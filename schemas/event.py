from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from schemas import DatetimeSchema
from schemas.location import CityResponse
from utils.enums import StatusEnum


class EventBase(BaseModel):
    name: str
    description: str
    date: datetime
    capacity: int
    status: StatusEnum
    location_id: int
    category_id: int
    owner_id: int


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    status: Optional[StatusEnum] = None
    

class EventCreate(EventBase):
    pass


class EventResponse(EventBase, DatetimeSchema):
    id: int
    location: CityResponse

    class Config:
        orm_mode = True


class EventTicketBase(BaseModel):
    event_id: int
    user_id: int


class EventTicketCreate(EventTicketBase):
    pass


class EventTicketResponse(EventTicketBase, DatetimeSchema):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    capacity: int
    speaker: str


class SessionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    speaker: Optional[str] = None
    

class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase, DatetimeSchema):
    id: int
    event_id: int
    
    class Config:
        orm_mode = True

