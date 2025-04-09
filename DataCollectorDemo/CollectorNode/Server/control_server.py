from fastapi import FastAPI

from typing import Any

from CollectorNode.Server import Command
from CollectorNode.Server import ServerBase
from Common.Communication import ActivitySelection, MessageCategory


class ControlServer(ServerBase):
    """Central server for communication with the UI."""

    def __init__(self):
        super().__init__("ControlServer")

        self._servers: set[ServerBase] = set()

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


    def register_server(self, other_server: ServerBase, set_active_automatically: bool = True):
        """Register another server."""
        if other_server in self._servers:
            return

        self._servers.add(other_server)
        if set_active_automatically:
            other_server._active = self._active

    def get_server_names(self) -> tuple[str, ...]:
        server_names = tuple(x.name for x in self._servers)
        return server_names

    def is_online(self) -> bool:
        return self._active


server: ControlServer | None = None
app = FastAPI()

@app.post("/ControlServer")
def execute_command(cmd: Command) -> dict[MessageCategory, Any]:
    """
    Execute a command in the server.
    :param cmd: Command to execute.
    :return: Results from the execution. Error message if not executable. Ordered by OK, NOK, and NAs.
    """
    if server is None:
        return {MessageCategory.nok: "Server not initialized."}

    match cmd.type_:
        case ActivitySelection.get_info:
            match cmd.command:
                case "get_servers":
                    names = server.get_server_names()
                    return {MessageCategory.ok: names}
                case _:
                    return {MessageCategory.nok: "Command not found."}
        case ActivitySelection.action:
            match cmd.action:
                case "is_online":
                    is_online: bool = server.is_online()
                    return {MessageCategory.ok: is_online}
                case "activate":
                    server.activate()
                    return {MessageCategory.ok: None}
                case "deactivate":
                    server.deactivate()
                    return {MessageCategory.ok: None}
                case _:
                    return {MessageCategory.nok: "Command not found."}
        case _:
            return {MessageCategory.nok: "Category not applicable in this context."}

