import abc
from abc import abstractmethod
from Common.Communication import Command
from Common.Communication import Response


class ServerBase(abc.ABC):
    """BaseNode class for all servers."""
    def __init__(self, name: str):
        self._name: str = name
        self._server_active: bool = False
        self._shutdown_finished: bool = False

    def __del__(self):
        self.shutting_down()

    @property
    def name(self) -> str:
        """Get the name of the server. This is used for the display of the """
        return self._name

    @abstractmethod
    def execute_command(self, command: Command) -> Response:
        pass

    @property
    @abstractmethod
    def server_namespace(self) -> str:
        """
        Get the namespace for that particular server. This is used for addressing components, hence for automated
        usages. If displayed, use "name" instead.
        """
        pass

    @property
    def _active(self):
        """Whether the server is active."""
        return self._server_active

    @_active.setter
    def _active(self, value: bool):
        self._server_active = value

    @property
    @abstractmethod
    def is_online(self):
        """Whether the server is active. Difference to :attr ServerBase._active: is that
         this checks that all conditions are met to be online, i.e., that all resources are available."""
        pass

    def shutting_down(self):
        if self._shutdown_finished:
            return
        self.shutdown()
        self._shutdown_finished = True

    @abstractmethod
    def shutdown(self):
        """Shut down the server."""
        pass

    @abstractmethod
    def on_new_data(self, dataset):
        pass
