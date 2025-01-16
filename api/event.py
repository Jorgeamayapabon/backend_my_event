from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.config import get_db
from models.event import EventModel
from models.user import UserModel
from schemas.event import (
    EventCreate,
    EventResponse,
    EventTicketCreate,
    EventTicketResponse,
    EventUpdate,
    SessionCreate,
    SessionResponse,
)
from services.elasticsearch_services import index_event_with_relations, search_events
from services.event_services import EventServiceHandler
from utils.auths import get_current_user, get_current_user_with_role
from utils.enums import StatusEnum


event_router = APIRouter()
session_router = APIRouter()


@event_router.get("", response_model=List[EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(
        get_current_user_with_role(["admin", "owner", "assistant"])
    ),
    name: Optional[str] = Query(None, description="Filter by event name"),
    min_date: Optional[datetime] = Query(None, description="Filter by minimum date"),
    max_date: Optional[datetime] = Query(None, description="Filter by maximum date"),
    status: Optional[StatusEnum] = Query(None, description="Filter by status"),
    location_id: Optional[int] = Query(None, description="Filter by location ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, description="Maximum number of records to retrieve"),

):
    """
    Retrieve a list of all events.
    
    Args:
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin", "owner", or "assistant".
        min_date (Optional[datetime], optional): Filter by minimum date. Defaults to None.
        max_date (Optional[datetime], optional): Filter by maximum date. Defaults to None.
        status (Optional[StatusEnum], optional): Filter by status. Defaults to None.
        location_id (Optional[int], optional): Filter by location ID. Defaults to None.
        category_id (Optional[int], optional): Filter by category ID. Defaults to None.

    Returns:
        List[EventResponse]: A list of event objects.
    """
    service = EventServiceHandler(db)
    return service.filter_events(
        name=name,
        min_date=min_date,
        max_date=max_date,
        status=status,
        location_id=location_id,
        category_id=category_id,
        offset=offset,
        limit=limit,
    )


@event_router.post("", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Create a new event.

    Args:
        event (EventCreate): The data required to create an event.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        EventResponse: The newly created event object.
    """
    service = EventServiceHandler(db)
    return service.create_event(event)


@event_router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(
        get_current_user_with_role(["admin", "owner", "assistant"])
    ),
):
    """
    Retrieve details of a specific event.

    Args:
        event_id (int): ID of the event to retrieve.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin", "owner", or "assistant".

    Returns:
        EventResponse: The event object with the given ID.
    """
    service = EventServiceHandler(db)
    return service.get_event_by_id(event_id)


@event_router.patch("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Update an existing event.

    Args:
        event_id (int): ID of the event to update.
        event (EventUpdate): The updated data for the event.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        EventResponse: The updated event object.
    """
    service = EventServiceHandler(db)
    return service.update_event(
        event_id=event_id,
        event=event,
        current_user=current_user,
    )


@event_router.delete("/{event_id}", response_model=EventResponse)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Delete an event.

    Args:
        event_id (int): ID of the event to delete.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        EventResponse: The deleted event object.
    """
    service = EventServiceHandler(db)
    return service.delete_event(
        event_id=event_id,
        current_user=current_user,
    )


@event_router.post("/ticket/{event_id}", response_model=EventTicketResponse)
def create_ticket(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["assistant"])),
):
    """
    Create a ticket for a specific event.

    Args:
        event_id (int): ID of the event for which to create a ticket.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the role "assistant".

    Returns:
        EventTicketResponse: The created ticket object.
    """
    service = EventServiceHandler(db)
    return service.create_ticket(event_id, current_user)


@session_router.get("/{event_id}", response_model=List[SessionResponse])
def list_sessions_by_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(
        get_current_user_with_role(["admin", "owner", "assistant"])
    ),
):
    """
    List all sessions for a specific event.

    Args:
        event_id (int): ID of the event whose sessions to retrieve.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin", "owner", or "assistant".

    Returns:
        List[SessionResponse]: A list of sessions for the given event.
    """
    service = EventServiceHandler(db)
    return service.list_sessions_by_event(event_id)
