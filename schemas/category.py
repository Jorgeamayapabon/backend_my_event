from pydantic import BaseModel

from schemas import DatetimeSchema


class CategoryBase(BaseModel):
    name: str
    

class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase, DatetimeSchema):
    id: int
    
    class Config:
        orm_mode = True
