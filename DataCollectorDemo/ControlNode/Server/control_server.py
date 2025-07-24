from typing import Callable

import httpx

from Common.Communication import CommandModel, ResponseModel, ResponseFactory
from BaseNode.Server.server_base import ServerBase
from Common.Model import ServerOutline

NAMESPACE: str = "ControlServer"

class ControlServer(ServerBase):
    """Central server for communication with the UI."""

    def get_outline(self) -> ServerOutline:
        return ServerOutline(
            port=self.port,
            name=self.name
        )

    def on_new_data(self, dataset):
        pass

    def __init__(self):
        super().__init__(NAMESPACE, 8000)
        self._register_callbacks: list[Callable[[str], None]] = []
        self._servers: set[ServerOutline] = set()
        self._data_sources: set[ServerOutline] = set()
        self._data_receivers: set[ServerOutline] = set()

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


    def register_server(self, other_server: ServerOutline, set_active_automatically: bool = True,
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
        if other_server.sensor_data_sender:
            self._data_sources.add(other_server)

        if other_server.sensor_data_receiver:
            self._data_receivers.add(other_server)

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

    async def publish_command(self, command: CommandModel) -> ResponseModel:
        target: ServerOutline | None = next((x for x in self._servers if x.name == command.target), None)
        if target is None:
            return ResponseFactory.nok("Target server not found.")

        address: str = f"http://localhost:{target.port}/{command.command}"

        async with httpx.AsyncClient() as client:
            try:
                if command.parameters is None:
                    http_response = await client.post(address)
                else:
                    payload = command.parameters.model_dump()
                    http_response = await client.post(address, json=payload)

                response: ResponseModel = ResponseModel(**(http_response.json()))
            except Exception as e:
                print(f"Converting not successful: {e}")
                return ResponseFactory.nok(repr(e))

            return response




