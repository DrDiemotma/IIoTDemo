from typing import Any, Callable

from Common.Communication import Command, MessageCategory, Response, ResponseFactory
from CollectorNode.Server.server_base import ServerBase
from Common.Communication.activity_selection import ActivitySelection


NAMESPACE: str = "ControlServer"

class ControlServer(ServerBase):
    """Central server for communication with the UI."""

    def on_new_data(self, dataset):
        pass

    @property
    def server_namespace(self):
        return NAMESPACE

    def __init__(self):
        super().__init__("ControlServer")
        self._register_callbacks: list[Callable[[str], None]] = []
        self._servers: set[ServerBase] = set()

    def __del__(self):
        if self.is_online:
            self.deactivate()

    def activate(self):
        """Activate the servers."""
        if self._active:
            return
        for other_server in self._servers:
            other_server._active = True

        self._active = True

    def deactivate(self):
        """Deactivate the server."""
        if not self._active:
            return

        for other_server in self._servers:
            other_server._active = False

        self._active = False


    def register_server(self, other_server: ServerBase, set_active_automatically: bool = True,
                        register_callback: Callable[[str], None] | None = None):
        """
        Register another server.
        :param other_server: Server to register.
        :param set_active_automatically: Whether it should follow the activity state of the control server.
        :param register_callback: Callback for when another service is registered.
        """
        if other_server in self._servers:
            return

        self._servers.add(other_server)
        if set_active_automatically:
            other_server._active = self._active

        self.on_new_register(other_server.name)

        if register_callback is not None:
            self._register_callbacks.append(register_callback)

    def get_server_names(self) -> tuple[str, ...]:
        """
        Get the names of the registered services.
        :return: a tuple of registered names.
        """
        server_names = tuple(x.name for x in self._servers)
        return server_names

    @property
    def is_online(self) -> bool:
        return self._active

    def on_new_register(self, name: str):
        for callback in self._register_callbacks:
            callback(name)

    def shutdown(self):
        pass

    async def get_mainloop(self):
        pass

    def _execute(self, cmd: Command) -> Response:
        match cmd.type_:
            case ActivitySelection.get_info:
                match cmd.command:
                    case "get_servers":
                        names = self.get_server_names()
                        return ResponseFactory.ok(values=names)
                    case _:
                        return ResponseFactory.nok("Command not found.")
            case ActivitySelection.action:
                match cmd.action:
                    case "is_online":
                        is_online: bool = self.is_online
                        return ResponseFactory.ok(values=is_online)
                    case "activate":
                        self.activate()
                        return ResponseFactory.ok()
                    case "deactivate":
                        self.deactivate()
                        return ResponseFactory.ok()
                    case "shutdown":
                        self.shutdown()
                        return ResponseFactory.ok()
                    case _:
                        return ResponseFactory.nok("Command not found")
            case _:
                return ResponseFactory.nok("Category not applicable in this context.")


    def execute_command(self, cmd: Command) -> Response:
        """
        Execute a command in the server.
        :param cmd: Command to execute.
        :return: Results from the execution. Error message if not executable. Ordered by OK, NOK, and NAs.
        """

        target: str = cmd.target
        if target == self.server_namespace:
            return self._execute(cmd)

        target_server = next((x for x in self._servers if x.server_namespace == target), None)
        if target_server is None:
            # return {MessageCategory.nok: "Service not found"}
            return Response(message_result=MessageCategory.nok, return_message="Service not found")

        return target_server.execute_command(cmd)



