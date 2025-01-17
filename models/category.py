from sqlalchemy import Column, Integer, String
from db.config import Base
from sqlalchemy.orm import relationship

from models.base import DatetimeModel


class CategoryModel(Base, DatetimeModel):
    """
    Represents a category in the database.

    This model extends the `DatetimeModel` to include timestamps (`created_at` and `updated_at`) 
    and provides attributes for managing category data.

    Attributes:
        id (Column): The primary key of the category.
        name (Column): The name of the category.
        events (relationship): A relationship to the `EventModel`, allowing access to events
            associated with this category.
    """
    __tablename__ = "category"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True, 
        doc="The unique identifier for the category."
    )
    name = Column(
        String, 
        index=True, 
        doc="The name of the category, used for display and identification."
    )
