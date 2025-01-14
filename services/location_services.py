from sqlalchemy.orm import Session

from models.location import CityModel, CountryModel


class LocationServiceHandler:
    def __init__(self, db: Session):
        self.db = db
    
    def list_countries(self):
        return self.db.query(CountryModel).all()
    
    def list_cities(self):
        return self.db.query(CityModel).all()
    
    def create_country(self, country):
        db_country = CountryModel(**country.dict())
        self.db.add(db_country)
        self.db.commit()
        self.db.refresh(db_country)
        return db_country
    
    def create_city(self, city):
        db_city = CityModel(**city.dict())
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city
