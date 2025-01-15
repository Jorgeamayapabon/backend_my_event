from sqlalchemy.orm import Session

from models.location import CityModel, CountryModel


class LocationServiceHandler:
    """
    Handles location-related operations, including managing countries and cities.

    Attributes:
        db (Session): The database session used to interact with the database.
    """
    
    def __init__(self, db: Session):
        """
        Initializes the location service handler with a database session.

        Args:
            db (Session): The database session used to interact with the database.
        """
        self.db = db
    
    def list_countries(self):
        """
        Retrieves a list of all countries.

        Returns:
            list: A list of all countries from the database.
        """
        return self.db.query(CountryModel).all()
    
    def list_cities(self):
        """
        Retrieves a list of all cities.

        Returns:
            list: A list of all cities from the database.
        """
        return self.db.query(CityModel).all()
    
    def create_country(self, country):
        """
        Creates a new country in the database.

        Args:
            country: A schema object representing the country to be created.

        Returns:
            CountryModel: The created country.

        Raises:
            ValidationError: If the country data is invalid.
        """
        db_country = CountryModel(**country.dict())
        self.db.add(db_country)
        self.db.commit()
        self.db.refresh(db_country)
        return db_country
    
    def create_city(self, city):
        """
        Creates a new city in the database.

        Args:
            city: A schema object representing the city to be created.

        Returns:
            CityModel: The created city.

        Raises:
            ValidationError: If the city data is invalid.
        """
        db_city = CityModel(**city.dict())
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city
