from sqlalchemy import Boolean, Column, Integer, String, Enum as SQLAlchemyEnum
from db.config import Base
from sqlalchemy.orm import relationship

from models.base import DatetimeModel
from utils.enums import RoleEnum


class UserModel(Base, DatetimeModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    hashed_password = Column(String, nullable=False)

    events = relationship("EventModel", back_populates="owner")
    