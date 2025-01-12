from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    code: str


class CountryCreate(CountryBase):
    pass


class CountryResponse(CountryBase):
    id: int

    class Config:
        orm_mode = True


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    country_id: int
    
    
class CityResponse(CityBase):
    id: int
    country: CountryResponse
    
    class Config:
        orm_mode = True
