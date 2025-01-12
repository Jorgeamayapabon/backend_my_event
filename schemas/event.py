from datetime import datetime
from pydantic import BaseModel

from schemas.location import CityResponse


class EventBase(BaseModel):
    name: str
    description: str
    date: datetime
    capacity: int
    location_id: int
    category_id: int
    owner_id: int


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    location: CityResponse

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    capacity: int
    speaker: str
    

class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase):
    id: int
    
    class Config:
        orm_mode = True
