from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from models.user import UserModel
from schemas.location import CityCreate, CityResponse, CountryCreate, CountryResponse
from services.location_services import LocationServiceHandler
from utils.auths import get_current_user_with_role


router = APIRouter()


@router.get("/country", response_model=List[CountryResponse])
def list_countries(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = LocationServiceHandler(db)
    return service.list_countries()


@router.post("/country", response_model=CountryResponse)
def create_country(
    country: CountryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = LocationServiceHandler(db)
    return service.create_country(country)


@router.get("/city", response_model=CityResponse)
def list_cities(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = LocationServiceHandler(db)
    service.list_cities()


@router.post("/city", response_model=CityResponse)
def create_city(
    city: CityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    service = LocationServiceHandler(db)
    return service.create_city(city)
