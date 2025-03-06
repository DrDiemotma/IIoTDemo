from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Optional

class Command(BaseModel):
    action: str
    parameters: Optional[list[Any]] = None




class ControlServer:

    def __init__(self):
        self._started = False

    def add_config(self, config_json: str):
        pass

    def select_client(self, ip_address: str, port: int):
        pass

    def is_online(self) -> bool:
        return self._started

    def activate(self):
        self._started = True

    def deactivate(self):
        self._started = False



server: ControlServer | None = None
app = FastAPI()

@app.post("/ControlServer")
def execute_command(cmd: Command) -> dict[str, Any]:
    if server is None:
        return {"error": "Server not initialized."}

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

