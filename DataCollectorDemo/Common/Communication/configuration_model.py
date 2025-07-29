from pydantic import BaseModel
from typing import Any

class ConfigurationModel(BaseModel):
    entries: dict[str, Any]

    class Config:
        frozen = True
