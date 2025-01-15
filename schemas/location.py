from pydantic import BaseModel

from schemas import DatetimeSchema


class CountryBase(BaseModel):
    """
    A base schema for country-related operations.

    This schema defines the core attributes for a country model, used in the creation 
    or updating of country records.

    Attributes:
        name (str): The name of the country.
        code (str): The country code (e.g., 'US', 'CO').
    """
    name: str
    code: str


class CountryCreate(CountryBase):
    """
    A schema for creating a new country.

    Inherits from `CountryBase` and does not add any new attributes.
    It is used for request bodies when creating a new country.

    Attributes:
        name (str): The name of the country (inherited from CountryBase).
        code (str): The country code (inherited from CountryBase).
    """
    pass


class CountryResponse(CountryBase, DatetimeSchema):
    """
    A schema for representing a country in response data.

    This schema includes country information along with timestamps for creation and 
    updates. It inherits from both `CountryBase` and `DatetimeSchema`.

    Attributes:
        id (int): The unique identifier for the country.
        name (str): The name of the country (inherited from CountryBase).
        code (str): The country code (inherited from CountryBase).
        created_at (datetime): The timestamp when the country was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the country was last updated (inherited from DatetimeSchema).
    """
    id: int

    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True


class CityBase(BaseModel):
    """
    A base schema for city-related operations.

    This schema defines the core attributes for a city model, used in the creation 
    or updating of city records.

    Attributes:
        name (str): The name of the city.
    """
    name: str


class CityCreate(CityBase):
    """
    A schema for creating a new city.

    This schema adds the `country_id` attribute for creating a city under a specific country.

    Attributes:
        name (str): The name of the city (inherited from CityBase).
        country_id (int): The ID of the country the city belongs to.
    """
    country_id: int


class CityResponse(CityBase, DatetimeSchema):
    """
    A schema for representing a city in response data.

    This schema includes city information along with timestamps for creation and 
    updates. It also includes the associated country data.

    Attributes:
        id (int): The unique identifier for the city.
        name (str): The name of the city (inherited from CityBase).
        country (CountryResponse): The country to which the city belongs.
        created_at (datetime): The timestamp when the city was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the city was last updated (inherited from DatetimeSchema).
    """
    id: int
    country: CountryResponse

    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True
