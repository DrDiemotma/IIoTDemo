from pydantic import BaseModel
from typing import Optional
from Common.Communication import ActivitySelection

class CommandModel(BaseModel):
    """
    Command class for communication between services.
    """
    sender: str
    """Name of the sender."""
    target: str
    """Target server component."""
    type_: ActivitySelection = ActivitySelection.action
    """Type of the command as a string."""
    command: str
    """Command to execute."""
    parameters: Optional[BaseModel] = None
    """Parameters for the command to execute on the server."""

    def __str__(self):
        if self.parameters is None:
            return f"From {self.sender} to {self.target} ({self.type_}): {self.command}"
        return f"From {self.sender} to {self.target} ({self.type_}): {self.command} ({self.parameters})"

    class Config:
        frozen = True
