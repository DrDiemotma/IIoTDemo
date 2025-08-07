from pydantic import BaseModel, Field
from datetime import datetime
from enum import StrEnum


class SeverityClass(StrEnum):
    """Severity of the message"""
    INFO = "info"
    """Info level. No action necessary."""
    WARNING = "warning"
    """Warning level. An action might be necessary."""
    ERROR = "error"
    """Error level: something went wrong."""

class MessageSeverity(BaseModel):
    """Message severity class. While OPC UA uses an increasing integer of severity, an error becomes arbitrary.
    Here, each of the three categories can have its own range from 0 to 100."""
    severity_level: SeverityClass = SeverityClass.INFO
    """The Severity of the message."""
    impact: int = Field(..., ge=0, le=100)
    """Implications on the context of the message."""
    model_config = {
        "frozen": True
    }

class EvaluationModel(BaseModel):
    """Messaging type for evaluations."""
    machine_id: str | int
    """Machine ID."""
    description: str
    """Description of the evaluation."""
    timestamp: datetime
    """Time stamp of the evaluation."""
    severity: MessageSeverity = Field(default_factory=MessageSeverity)
    data_package:dict | list | None = None

    model_config = {
        "frozen": True
    }
