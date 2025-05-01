from typing import Optional, Any, Self
from pydantic import BaseModel
from sympy import andre

from Common.Communication import MessageCategory


class Response(BaseModel):
    """
    Response of action
    """
    message_result: MessageCategory
    """Message category: ok, nok, or na."""
    return_values: Optional[Any] = None
    """Return values, if any."""
    return_message: Optional[str] = None

    def __str__(self):
        if self.return_values is None:
            return f"{self.message_result}"
        return f"{self.message_result}: {self.return_values}"


class ResponseFactory:
    @staticmethod
    def ok(message: str | None = None, values: Any = None) -> Response:
        if message is None and values is None:
            return Response(message_result=MessageCategory.ok)
        if values is None:
            return Response(message_result=MessageCategory.ok, return_message=message)
        if message is None:
            return Response(message_result=MessageCategory.ok, return_values=values)
        return Response(message_result=MessageCategory.ok, return_message=message, return_values=values)

    @staticmethod
    def nok(message: str, values: Any = None):
        if values is None:
            return Response(message_result=MessageCategory.nok, return_message=message)
        return Response(message_result=MessageCategory.nok, return_message=message, return_values=values)
