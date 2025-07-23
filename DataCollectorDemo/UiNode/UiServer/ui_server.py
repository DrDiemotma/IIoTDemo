from BaseNode.Server import ServerBase
from Common.Communication import Command, ActivitySelection, MessageCategory, ResponseModel, ResponseFactory
from typing import Any

from Common.Model import ServerOutline

NAME: str = "UiServer"
class UiServer(ServerBase):

    def get_outline(self) -> ServerOutline:
        return ServerOutline(
            name=self.name,
            port=self.port
        )

    def shutdown(self):
        pass

    _settings: dict[str, Any]

    def execute_command(self, command: Command) -> ResponseModel:
        """
        Execute the command. Known commands: "register" and "get_value".
        :param command: Command to execute.
        :return:
        """
        if command.type_ is not ActivitySelection.action:
            return ResponseModel(message_result=MessageCategory.nok, return_value="Info not implemented.")

        match command.command:
            case "register":
                name = command.parameters[0]
                self.register(name, *command.parameters[1:])

                return ResponseModel(message_result=MessageCategory.ok)
            case "get_value":
                name = command.parameters

        return ResponseFactory.nok("Command not found.")

    def __init__(self):
        super().__init__(NAME, port=8012)
        self._settings: dict[str, Any] = {}

    def on_new_data(self, dataset):
        pass

    @property
    def is_online(self):
        return True  # UI server is always online

    @property
    def server_namespace(self):
        return NAME

    def register(self, key: str, value: int | float | str | list[int | float | str], override = False) -> bool:
        if not override and key in self._settings:
            return False

        self._settings[key] = value
        return True

    def get_value(self, key: str) -> int | float | str | list[int | float | str] | None:
        if key not in self._settings:
            return None

        return self._settings[key]


