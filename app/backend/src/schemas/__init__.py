from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Candle(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class Workflow(BaseModel):
    id: UUID
    name: str
    json: dict
