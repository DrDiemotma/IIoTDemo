from dataclasses import dataclass
import pandas as pd
from typing import Any, Optional


@dataclass(frozen=True)
class DataEntry:
    name: str
    data: Any

    def __str__(self):
        return f"{self.name}: {self.data}"

@dataclass(frozen=True)
class Data:
    measured_time: pd.Timestamp
    received_time: pd.Timestamp
    data_field: DataEntry

@dataclass(frozen=True)
class DataPackage:
    data_fields: set[Data] = set[Data]

    @property
    def start_measured_time(self) -> pd.Timestamp | None:
        if len(self.data_fields) == 0:
            return None
        return min(x.measured_time for x in self.data_fields)

    @property
    def stop_measured_time(self) -> pd.Timestamp | None:
        if len(self.data_fields) == 0:
            return None
        return max(x.measured_time for x in self.data_fields)

    @property
    def start_recorded_time(self) -> pd.Timestamp | None:
        if len(self.data_fields) == 0:
            return None
        return min(x.received_time for x in self.data_fields)

    @property
    def stop_recorded_time(self) -> pd.Timestamp | None:
        if len(self.data_fields) == 0:
            return None
        return max(x.measured_time for x in self.data_fields)

@dataclass(frozen=True)
class ConfigData:
    """Data entry for configuration"""
    property_name: str
    property_value: str | int | float | list[str | int | float]

@dataclass(frozen=True)
class ConfigSet:
    """Set of configurations."""
    items: set[ConfigData]
    """Configuration items"""
    target: Optional[str] = None

