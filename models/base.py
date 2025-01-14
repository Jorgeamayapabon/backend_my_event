from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


class DatetimeModel:
    __abstract__ = True
    
    create_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
