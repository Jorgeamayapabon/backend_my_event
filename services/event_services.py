from fastapi import HTTPException, status
from models.event import EventModel, EventTicketModel, SessionModel
from models.user import UserModel
from schemas.event import EventCreate, EventUpdate, SessionCreate

from sqlalchemy.orm import Session


class EventServiceHandler:
    def __init__(self, db: Session):
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
        return self.db.query(EventModel).all()

    def create_event(self, event: EventCreate):
        event = EventModel(**event.model_dump())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
    
    def get_event_by_id(self, event_id: int):
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        return db_event
        
    def update_event(self, event_id: int, event: EventUpdate, current_user: UserModel):
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
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        self.db.delete(db_event)
        self.db.commit()
        return db_event
    
    def create_ticket(self, event_id: int, current_user: UserModel):
        event_ticket = EventTicketModel(
            event_id=event_id,
            user_id=current_user.id
        )
        self.db.add(event_ticket)
        self.db.commit()
        self.db.refresh(event_ticket)
        return event_ticket
    
    def list_sessions_by_event(self, event_id: int):
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not db_event:
            raise self._event_not_found
        
        return db_event.sessions
    
    def list_all_sessions(self):
        return self.db.query(SessionModel).all()
    
    def create_session(self, event_id: int, session: SessionCreate, current_user: UserModel):
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
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise self._session_not_found
        
        return db_session
    
    def update_session(self, session_id: int, session: SessionCreate, current_user: UserModel):
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
        db_session = self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not db_session:
            raise self._session_not_found
        
        db_event = self.get_event_by_id(db_session.event_id)
        
        if db_event.owner_id != current_user.id:
            raise self._forbidden_by_no_owner
        
        self.db.delete(db_session)
        self.db.commit()
        return db_session
