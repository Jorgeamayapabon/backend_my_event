from typing import List
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


event_router = APIRouter()
session_router = APIRouter()


@event_router.get("", response_model=List[EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(
        get_current_user_with_role(["admin", "owner", "assistant"])
    ),
):
    service = EventServiceHandler(db)
    return service.list_events()


@event_router.post("", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
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
    service = EventServiceHandler(db)
    return service.get_event_by_id(event_id)


@event_router.patch("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
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
    service = EventServiceHandler(db)
    return service.list_sessions_by_event(event_id)


@session_router.get("", response_model=List[SessionResponse])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(
        get_current_user_with_role(["admin", "owner", "assistant"])
    ),
):
    service = EventServiceHandler(db)
    return service.list_all_sessions()


@session_router.post("/{event_id}", response_model=SessionResponse)
def create_session(
    event_id: int,
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = EventServiceHandler(db)
    return service.create_session(
        event_id=event_id, session=session, current_user=current_user
    )


@session_router.patch("/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int,
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = EventServiceHandler(db)
    return service.update_session(
        session_id=session_id, session=session, current_user=current_user
    )


@session_router.delete("/{session_id}", response_model=SessionResponse)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = EventServiceHandler(db)
    return service.delete_session(session_id=session_id, current_user=current_user)


@event_router.post("/index/{event_id}")
def index_event(event_id: int, db: Session = Depends(get_db)):
    service = EventServiceHandler(db)
    db_event = service.get_event_by_id(event_id)
    index_event_with_relations(db_event, db)
    return {"message": "Event indexed successfully"}


def get_filters(
    status: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    category_name: str = Query(None),
    location_name: str = Query(None)
) -> dict:
    filters = {}
    if status:
        filters["status"] = status
    if date_from and date_to:
        filters["date"] = {"gte": date_from, "lte": date_to}
    if category_name:
        filters["category_name"] = category_name
    if location_name:
        filters["location_name"] = location_name
    return filters

@event_router.post("/search")
def index_event(query: str, filters: dict = Depends(get_filters)):
    results = search_events(query, filters)
    return {"results": results}
