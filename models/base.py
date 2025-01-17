from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


class DatetimeModel:
    """
    Abstract base class for SQLAlchemy models with timestamp fields.

    This class provides two common fields for tracking when a record was created and last updated.
    - `created_at`: Automatically set to the current UTC time when the record is created.
    - `updated_at`: Automatically updated to the current UTC time whenever the record is modified.

    Attributes:
        created_at (Column): The datetime when the record was created.
        updated_at (Column): The datetime when the record was last updated.
    """
    __abstract__ = True

    created_at = Column(
        DateTime, 
        default=datetime.now(timezone.utc),
        doc="The datetime when the record was created, in UTC."
    )
    updated_at = Column(
        DateTime, 
        default=datetime.now(timezone.utc), 
        onupdate=datetime.now(timezone.utc),
        doc="The datetime when the record was last updated, in UTC."
    )
