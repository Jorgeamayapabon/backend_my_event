from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from models.user import UserModel
from schemas.location import CityCreate, CityResponse, CountryCreate, CountryResponse
from services.location_services import LocationServiceHandler
from utils.auths import get_current_user_with_role

# Create a router for location-related endpoints
router = APIRouter()


@router.get("/country", response_model=List[CountryResponse])
def list_countries(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Retrieve a list of all countries.

    Args:
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        List[CountryResponse]: A list of country objects.
    """
    service = LocationServiceHandler(db)
    return service.list_countries()


@router.post("/country", response_model=CountryResponse)
def create_country(
    country: CountryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Create a new country.

    Args:
        country (CountryCreate): The data required to create a country.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        CountryResponse: The newly created country object.
    """
    service = LocationServiceHandler(db)
    return service.create_country(country)


@router.get("/city", response_model=CityResponse)
def list_cities(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Retrieve a list of all cities.

    Args:
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        List[CityResponse]: A list of city objects.
    """
    service = LocationServiceHandler(db)
    return service.list_cities()  # Fixed the missing return statement


@router.post("/city", response_model=CityResponse)
def create_city(
    city: CityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Create a new city.

    Args:
        city (CityCreate): The data required to create a city.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        CityResponse: The newly created city object.
    """
    service = LocationServiceHandler(db)
    return service.create_city(city)
