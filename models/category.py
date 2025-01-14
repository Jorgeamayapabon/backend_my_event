from sqlalchemy import Column, Integer, String
from db.config import Base
from sqlalchemy.orm import relationship

from models.base import DatetimeModel


class CategoryModel(Base, DatetimeModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    events = relationship("EventModel", back_populates="category")
