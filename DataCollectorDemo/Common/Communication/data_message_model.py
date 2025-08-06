from pydantic import BaseModel
from typing import Optional
from datetime import datetime

SensorValue = int | float | bool | str | \
    list[int | float | bool | str] | \
    dict[str | int, int | float | bool | str | list | dict]


class DataMessageModel(BaseModel):
    """Data model for transfer within the system."""
    name: str
    """Name of the value."""
    timestamp: datetime
    """Reading time of the sensor value."""
    value: SensorValue
    """Reading of the sensor."""
    server_timestamp: Optional[datetime] = None
    """Time stamp of the server if that is different from the reading time."""
    identifier: Optional[int] = None
    """Can be used for faster identification of measurement."""

    class Config:
        frozen = True
