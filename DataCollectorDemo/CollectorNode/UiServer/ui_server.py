from CollectorNode.Server import ServerBase
from Common.Communication import Command, ActivitySelection, MessageCategory, Response, ResponseFactory
from typing import Any

NAME: str = "UiServer"
class UiServer(ServerBase):

    def shutdown(self):
        self._server_active = False

    _settings: dict[str, Any]

    def execute_command(self, command: Command) -> Response:
        """
        Execute the command. Known commands: "register" and "get_value".
        :param command: Command to execute.
        :return:
        """
        if command.type_ is not ActivitySelection.action:
            return Response(message_result=MessageCategory.nok, return_values="Info not implemented.")

        match command.command:
            case "register":
                name = command.parameters[0]
                self.register(name, *command.parameters[1:])

                return Response(message_result=MessageCategory.ok)
            case "get_value":
                name = command.parameters

        return ResponseFactory.nok("Command not found.")

    def __init__(self):
        super().__init__(NAME)
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


