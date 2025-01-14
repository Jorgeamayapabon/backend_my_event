from db.config import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base import DatetimeModel


class CountryModel(Base, DatetimeModel):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, index=True)
    
    cities = relationship("CityModel", back_populates="country")


class CityModel(Base, DatetimeModel):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    
    country = relationship("CountryModel", back_populates="cities")	