from datetime import datetime, timezone
from sqlalchemy import Column, DateTime


class DatetimeModel:
    __abstract__ = True
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
