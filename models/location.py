from db.config import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base import DatetimeModel


class CountryModel(Base, DatetimeModel):
    """
    Represents a country in the system.

    This model extends the `DatetimeModel` to include timestamps (`created_at` and `updated_at`) 
    and provides attributes for managing country data, such as name and code. It also defines 
    a relationship to the `CityModel` to associate cities with their respective countries.

    Attributes:
        id (Column): The unique identifier for the country.
        name (Column): The name of the country.
        code (Column): A unique code for the country (e.g., country code).
        cities (relationship): A relationship to the `CityModel` for the cities within this country.
    """
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True, doc="The unique identifier for the country.")
    name = Column(String, index=True, doc="The name of the country.")
    code = Column(String, index=True, doc="A unique code for the country (e.g., country code).")
    
    # Relationship to the CityModel for cities in the country
    cities = relationship("CityModel", back_populates="country", doc="Relationship to the CityModel for the cities within this country.")


class CityModel(Base, DatetimeModel):
    """
    Represents a city in the system.

    This model extends the `DatetimeModel` to include timestamps and defines attributes 
    for managing city data, such as name and the associated country. It also establishes 
    a relationship to the `CountryModel` to link cities to their respective countries.

    Attributes:
        id (Column): The unique identifier for the city.
        name (Column): The name of the city.
        country_id (Column): The ID of the country where the city is located.
        country (relationship): A relationship to the `CountryModel` to associate the city with a country.
    """
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True, doc="The unique identifier for the city.")
    name = Column(String, index=True, doc="The name of the city.")
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False, doc="The ID of the country to which the city belongs.")
    
    # Relationship to the CountryModel for the associated country
    country = relationship("CountryModel", back_populates="cities", doc="Relationship to the CountryModel to link the city to its country.")
    events = relationship("EventModel", back_populates="location", doc="Relationship to the EventModel for events in the city.")
