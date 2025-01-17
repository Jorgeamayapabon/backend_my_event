from datetime import datetime
from pydantic import BaseModel


class DatetimeSchema(BaseModel):
    """
    A schema for managing timestamp data in Pydantic models.

    This schema contains two attributes, `created_at` and `updated_at`, 
    both of which are expected to be `datetime` objects. These attributes 
    are typically used to track when a resource was created and last updated.

    Attributes:
        created_at (datetime): The timestamp when the resource was created.
        updated_at (datetime): The timestamp when the resource was last updated.
    """
    created_at: datetime
    updated_at: datetime
