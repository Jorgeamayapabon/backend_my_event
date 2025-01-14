from datetime import datetime

from pydantic import BaseModel


class DatetimeSchema(BaseModel):
    create_at: datetime
    update_at: datetime
