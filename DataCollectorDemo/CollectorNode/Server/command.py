from pydantic import BaseModel
from typing import Any, Optional
from Common.Communication import ActivitySelection

class Command(BaseModel):
    """
    Command class for communication between services.
    """
    sender: str
    """Name of the sender."""
    type_: ActivitySelection
    """Type of the command as a string."""
    command: str
    """Command to execute."""
    parameters: Optional[list[Any]] = None
    """Parameters for the command to execute on the server."""
