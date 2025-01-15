from db.config import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from models.base import DatetimeModel
from utils.enums import StatusEnum


class EventModel(Base, DatetimeModel):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False)
    location_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    location = relationship("CityModel")
    category = relationship("CategoryModel")
    tickets = relationship("EventTicketModel", back_populates="event")
    sessions = relationship("SessionModel", back_populates="event")
    owner = relationship("UserModel", back_populates="events")


class SessionModel(Base, DatetimeModel):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    name = Column(String)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    capacity = Column(Integer)
    speaker = Column(String)

    event = relationship("EventModel", back_populates="sessions")


class EventTicketModel(Base, DatetimeModel):
    __tablename__ = "event_ticket"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    event = relationship("EventModel", back_populates="tickets")
    user = relationship("UserModel")
