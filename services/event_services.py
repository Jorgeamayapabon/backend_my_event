from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from models.category import CategoryModel
from models.event import EventModel, EventTicketModel, SessionModel
from models.location import CityModel
from models.user import UserModel
from schemas.event import EventCreate, EventUpdate, SessionCreate

from sqlalchemy.orm import Session, joinedload


class EventServiceHandler:
    """
    Handles all event-related operations, including event management and session management.

    Attributes:
        db (Session): The database session used to interact with the database.
        _event_not_found (HTTPException): Exception raised when an event is not found.
        _session_not_found (HTTPException): Exception raised when a session is not found.
        _forbidden_by_no_owner (HTTPException): Exception raised when the user is not the owner of the event.
    """
    
    def __init__(self, db: Session):
        """
        Initializes the service handler with a database session.

        Args:
            db (Session): The database session used to interact with the database.
        """
        self.db = db
        self._event_not_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
        self._session_not_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
        self._forbidden_by_no_owner = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not owner of this event"
        )

    def list_events(self):
        """
        Retrieves a list of all events.

        Returns:
            list: A list of all events from the database.
        """
        return self.db.query(EventModel).all()

    def create_event(self, event: EventCreate):
        """
        Creates a new event in the database.

        Args:
            event (EventCreate): The event data to create a new event.

        Returns:
            EventModel: The created event.
        """
        event = EventModel(**event.model_dump())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def get_event_by_id(self, event_id: int):
        """
        Retrieves an event by its ID.

        Args:
            event_id (int): The ID of the event to retrieve.

        Returns:
            EventModel: The event with the specified ID.

        Raises:
            HTTPException: If the event is not found.
        """
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        return db_event
        
    def update_event(self, event_id: int, event: EventUpdate, current_user: UserModel):
        """
        Updates an existing event by its ID.

        Args:
            event_id (int): The ID of the event to update.
            event (EventUpdate): The updated event data.
            current_user (UserModel): The current user performing the update.

        Returns:
            EventModel: The updated event.

        Raises:
            HTTPException: If the event is not found or if the current user is not the owner.
        """
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        event = event.model_dump()
        
        for key, value in event.items():
            setattr(db_event, key, value)
        
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def delete_event(self, event_id: int, current_user: UserModel):
        """
        Deletes an event by its ID.

        Args:
            event_id (int): The ID of the event to delete.
            current_user (UserModel): The current user performing the delete.

        Returns:
            EventModel: The deleted event.

        Raises:
            HTTPException: If the event is not found or if the current user is not the owner.
        """
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        self.db.delete(db_event)
        self.db.commit()
        return db_event
    
    def create_ticket(self, event_id: int, current_user: UserModel):
        """
        Creates a ticket for an event for a given user.

        Args:
            event_id (int): The ID of the event to create a ticket for.
            current_user (UserModel): The user who will receive the ticket.

        Returns:
            EventTicketModel: The created event ticket.
        """
        event_ticket = EventTicketModel(
            event_id=event_id,
            user_id=current_user.id
        )
        self.db.add(event_ticket)
        self.db.commit()
        self.db.refresh(event_ticket)
        return event_ticket
    
    def list_sessions_by_event(self, event_id: int):
        """
        Retrieves all sessions related to a specific event.

        Args:
            event_id (int): The ID of the event to retrieve sessions for.

        Returns:
            list: A list of sessions associated with the event.

        Raises:
            HTTPException: If the event is not found.
        """
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        return db_event.sessions
    
    def list_all_sessions(self):
        """
        Retrieves a list of all sessions.

        Returns:
            list: A list of all sessions from the database.
        """
        return self.db.query(SessionModel).all()
    
    def create_session(self, event_id: int, session: SessionCreate, current_user: UserModel):
        """
        Creates a new session for a specific event.

        Args:
            event_id (int): The ID of the event to create the session for.
            session (SessionCreate): The session data to create the new session.
            current_user (UserModel): The current user performing the creation.

        Returns:
            SessionModel: The created session.

        Raises:
            HTTPException: If the event is not found or if the current user is not the owner.
        """
        session_schema = session.model_dump()
        session_schema["event_id"] = event_id
        
        db_event = self.get_event_by_id(event_id)
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        db_session = SessionModel(**session_schema)
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    def get_session_by_id(self, session_id: int):
        """
        Retrieves a session by its ID.

        Args:
            session_id (int): The ID of the session to retrieve.

        Returns:
            SessionModel: The session with the specified ID.

        Raises:
            HTTPException: If the session is not found.
        """
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise self._session_not_found
        
        return db_session
    
    def update_session(self, session_id: int, session: SessionCreate, current_user: UserModel):
        """
        Updates an existing session by its ID.

        Args:
            session_id (int): The ID of the session to update.
            session (SessionCreate): The updated session data.
            current_user (UserModel): The current user performing the update.

        Returns:
            SessionModel: The updated session.

        Raises:
            HTTPException: If the session is not found or if the current user is not the owner.
        """
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise self._session_not_found
        
        db_event = self.get_event_by_id(db_session.event_id)
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        session = session.model_dump()
        
        for key, value in session.items():
            setattr(db_session, key, value)
        
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    def delete_session(self, session_id: int, current_user: UserModel):
        """
        Deletes a session by its ID.

        Args:
            session_id (int): The ID of the session to delete.
            current_user (UserModel): The current user performing the delete.

        Returns:
            SessionModel: The deleted session.

        Raises:
            HTTPException: If the session is not found or if the current user is not the owner.
        """
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise self._session_not_found
        
        db_event = self.get_event_by_id(db_session.event_id)
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        self.db.delete(db_session)
        self.db.commit()
        return db_session

    def filter_events(
        self,
        offset: int,
        limit: int,
        name: Optional[str] = None,
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None,
        status: Optional[str] = None,
        location_id: Optional[int] = None,
        category_id: Optional[int] = None,
    ):
        query = self.db.query(EventModel)
        
        # Agregar filtros dinámicos
        if name:
            query = query.filter(EventModel.name.ilike(f"%{name}%"))
        if min_date:
            query = query.filter(EventModel.date >= min_date)
        if max_date:
            query = query.filter(EventModel.date <= max_date)
        if status:
            query = query.filter(EventModel.status == status)
        if location_id:
            query = query.filter(EventModel.location_id == location_id)
        if category_id:
            query = query.filter(EventModel.category_id == category_id)

        return query.offset(offset).limit(limit).all()

    
    def filter_events_with_related_names(
        self,
        location_name: Optional[str] = None,
        category_name: Optional[str] = None,
        **filters
    ):
        query = self.db.query(EventModel).join(EventModel.location).join(EventModel.category)

        # Filtros relacionados
        if location_name:
            query = query.filter(CityModel.name.ilike(f"%{location_name}%"))
        if category_name:
            query = query.filter(CategoryModel.name.ilike(f"%{category_name}%"))

        # Filtros adicionales (usando los filtros dinámicos mencionados antes)
        for field, value in filters.items():
            if field == "offset" or field == "limit":
                continue
            
            if value is not None:
                query = query.filter(getattr(EventModel, field) == value)

        return query.options(
            joinedload(EventModel.location),
            joinedload(EventModel.category)
        ).offset(filters["offset"]).limit(filters["limit"]).all()
