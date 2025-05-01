from CollectorNode.OpcUaClient import OpcUaClient
from CollectorNode.Server import ServerBase
from Common.Communication import Command, Response


class OpcUaManagingServer(ServerBase):
    def shutdown(self):
        for client in self._clients:
            if client.is_connected():
                client.disconnect()

    def _configure_opc_ua_connection(self, dataset):
        pass

    def on_new_data(self, dataset):
        self._configure_opc_ua_connection(dataset)

    def execute_command(self, command: Command) -> Response:
        pass

    @property
    def server_namespace(self):
        return "OPCUA"

    def __init__(self):
        super().__init__("OpcUaManager")
        self._clients: list[OpcUaClient] = []

    @property
    def is_online(self):
        return self._active