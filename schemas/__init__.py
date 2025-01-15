from datetime import datetime

from pydantic import BaseModel


class DatetimeSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
