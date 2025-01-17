from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from schemas import DatetimeSchema
from schemas.location import CityResponse
from utils.enums import StatusEnum


class EventFilter(BaseModel):
    name: Optional[str]
    min_date: Optional[datetime]
    max_date: Optional[datetime]
    status: Optional[StatusEnum]
    location_id: Optional[int]
    category_id: Optional[int]


class EventBase(BaseModel):
    """
    A base schema for event-related operations.

    This schema defines the common attributes that all event models share. It is used 
    for creating or updating event records.

    Attributes:
        name (str): The name of the event.
        description (str): A brief description of the event.
        date (datetime): The date and time when the event is scheduled.
        capacity (int): The number of attendees the event can accommodate.
        status (StatusEnum): The current status of the event (e.g., 'active', 'inactive').
        location_id (int): The ID of the location where the event is held.
        category_id (int): The ID of the category to which the event belongs.
        owner_id (int): The ID of the user who owns the event.
    """
    name: str
    description: str
    date: datetime
    capacity: int
    status: StatusEnum
    location_id: int
    category_id: int
    owner_id: int


class EventUpdate(BaseModel):
    """
    A schema for updating an existing event.

    This schema is used for partial updates to an event's information. Each field is optional 
    to allow partial updates.

    Attributes:
        name (Optional[str]): The name of the event (optional).
        description (Optional[str]): A description of the event (optional).
        date (Optional[str]): The date and time of the event (optional).
        status (Optional[StatusEnum]): The status of the event (optional).
    """
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    status: Optional[StatusEnum] = None
   

class EventCreate(EventBase):
    """
    A schema for creating a new event.

    This schema inherits from `EventBase` and does not add any new attributes.
    It is used for request bodies when creating a new event.

    Attributes:
        name (str): The name of the event (inherited from EventBase).
        description (str): A description of the event (inherited from EventBase).
        date (datetime): The date and time of the event (inherited from EventBase).
        capacity (int): The number of attendees the event can accommodate (inherited from EventBase).
        status (StatusEnum): The status of the event (inherited from EventBase).
        location_id (int): The ID of the location (inherited from EventBase).
        category_id (int): The ID of the category (inherited from EventBase).
        owner_id (int): The ID of the owner (inherited from EventBase).
    """
    pass


class EventResponse(EventBase, DatetimeSchema):
    """
    A schema for representing an event in response data.

    This schema inherits from both `EventBase` and `DatetimeSchema`, 
    including the event information along with the timestamps for creation and updates.
    
    Attributes:
        id (int): The unique identifier for the event.
        name (str): The name of the event (inherited from EventBase).
        description (str): The description of the event (inherited from EventBase).
        date (datetime): The date of the event (inherited from EventBase).
        capacity (int): The capacity of the event (inherited from EventBase).
        status (StatusEnum): The status of the event (inherited from EventBase).
        location_id (int): The ID of the event's location (inherited from EventBase).
        category_id (int): The ID of the event's category (inherited from EventBase).
        owner_id (int): The ID of the event owner (inherited from EventBase).
        created_at (datetime): The timestamp when the event was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the event was last updated (inherited from DatetimeSchema).
        location (CityResponse): The location of the event as a nested response.
    """
    id: int
    location: CityResponse

    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True


class EventTicketBase(BaseModel):
    """
    A base schema for event ticket operations.

    This schema is used to represent the core information for an event ticket.

    Attributes:
        event_id (int): The ID of the associated event.
        user_id (int): The ID of the user associated with the ticket.
    """
    event_id: int
    user_id: int


class EventTicketCreate(EventTicketBase):
    """
    A schema for creating a new event ticket.

    Inherits from `EventTicketBase` and does not add any new attributes.
    It is used for request bodies when creating a new event ticket.

    Attributes:
        event_id (int): The ID of the event the ticket is for (inherited from EventTicketBase).
        user_id (int): The ID of the user who is purchasing the ticket (inherited from EventTicketBase).
    """
    pass


class EventTicketResponse(EventTicketBase, DatetimeSchema):
    """
    A schema for representing an event ticket in response data.

    This schema inherits from both `EventTicketBase` and `DatetimeSchema`, 
    providing ticket details along with the creation and update timestamps.
    
    Attributes:
        id (int): The unique identifier for the ticket.
        event_id (int): The ID of the event associated with the ticket (inherited from EventTicketBase).
        user_id (int): The ID of the user associated with the ticket (inherited from EventTicketBase).
        created_at (datetime): The timestamp when the ticket was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the ticket was last updated (inherited from DatetimeSchema).
    """
    id: int

    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True


class SessionBase(BaseModel):
    """
    A base schema for session-related operations.

    This schema defines the common attributes shared by session models. It is used 
    for creating or updating session records.

    Attributes:
        name (str): The name of the session.
        description (str): A description of the session.
        start_time (datetime): The start date and time for the session.
        end_time (datetime): The end date and time for the session.
        capacity (int): The number of attendees the session can accommodate.
        speaker (str): The name of the session's speaker.
    """
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    capacity: int
    speaker: str


class SessionUpdate(BaseModel):
    """
    A schema for updating an existing session.

    This schema is used for partial updates to a session's information. Each field is optional 
    to allow partial updates.

    Attributes:
        name (Optional[str]): The name of the session (optional).
        description (Optional[str]): The description of the session (optional).
        start_time (Optional[str]): The start date and time of the session (optional).
        end_time (Optional[str]): The end date and time of the session (optional).
        speaker (Optional[str]): The name of the session's speaker (optional).
    """
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    speaker: Optional[str] = None
   

class SessionCreate(SessionBase):
    """
    A schema for creating a new session.

    This schema inherits from `SessionBase` and does not add any new attributes.
    It is used for request bodies when creating a new session.

    Attributes:
        name (str): The name of the session (inherited from SessionBase).
        description (str): A description of the session (inherited from SessionBase).
        start_time (datetime): The start date and time for the session (inherited from SessionBase).
        end_time (datetime): The end date and time for the session (inherited from SessionBase).
        capacity (int): The capacity for the session (inherited from SessionBase).
        speaker (str): The speaker of the session (inherited from SessionBase).
    """
    pass


class SessionResponse(SessionBase, DatetimeSchema):
    """
    A schema for representing a session in response data.

    This schema inherits from both `SessionBase` and `DatetimeSchema`, 
    including the session information along with timestamps for creation and updates.

    Attributes:
        id (int): The unique identifier for the session.
        event_id (int): The ID of the associated event.
        name (str): The name of the session (inherited from SessionBase).
        description (str): The description of the session (inherited from SessionBase).
        start_time (datetime): The start date and time of the session (inherited from SessionBase).
        end_time (datetime): The end date and time of the session (inherited from SessionBase).
        capacity (int): The capacity of the session (inherited from SessionBase).
        speaker (str): The speaker of the session (inherited from SessionBase).
        created_at (datetime): The timestamp when the session was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the session was last updated (inherited from DatetimeSchema).
    """
    id: int
    event_id: int
    
    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True
