from datetime import datetime

from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    version: str
    datetime: datetime
