import abc


class ServerBase(abc.ABC):
    """Base class for all servers."""
    def __init__(self, name: str):
        self._name: str = name
        self._server_active: bool = False

    @property
    def name(self) -> str:
        """Get the name of the server."""
        return self._name

    @property
    def _active(self):
        """Whether the server is active."""
        return self._server_active

    @_active.setter
    def _active(self, value: bool):
        self._server_active = value
