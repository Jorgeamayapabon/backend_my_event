from db.config import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from models.base import DatetimeModel
from utils.enums import StatusEnum


class EventModel(Base, DatetimeModel):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    date = Column(Date)
    capacity = Column(Integer)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False)
    location_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    location = relationship("CityModel")
    category = relationship("CategoryModel")
    sessions = relationship("SessionModel", back_populates="event")
    owner = relationship("UserModel", back_populates="events")


class SessionModel(Base, DatetimeModel):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String)
    description = Column(Text)
    date = Column(Date)
    location = Column(String)
    capacity = Column(Integer)

    event = relationship("EventModel", back_populates="sessions")


class EventTicketModel(Base, DatetimeModel):
    __tablename__ = "event_tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    event = relationship("EventModel")
    user = relationship("UserModel")
