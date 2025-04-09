from altair.theme import active
from fastapi import FastAPI

from typing import Any

from CollectorNode.Server import Command
from CollectorNode.Server import ServerBase


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



    def add_config(self, config_json: str):
        pass

    def select_client(self, ip_address: str, port: int):
        pass

    def is_online(self) -> bool:
        return self._active





server: ControlServer | None = None
app = FastAPI()

@app.post("/ControlServer")
def execute_command(cmd: Command) -> dict[str, Any]:
    if server is None:
        return {"error": "Server not initialized."}

    match cmd.type_:
        case "":
            pass
    match cmd.action:
        case "add_config":
            server.add_config(*cmd.parameters)
            return {"ok": None}
        case "select_client":
            server.select_client(*cmd.parameters)
            return {"ok": None}
        case "is_online":
            is_online: bool = server.is_online()
            return {"ok": is_online}
        case "activate":
            server.activate()
            return {"ok": None}
        case "deactivate":
            server.deactivate()
            return {"ok": None}
        case _:
            return {"error": "Command not found."}

