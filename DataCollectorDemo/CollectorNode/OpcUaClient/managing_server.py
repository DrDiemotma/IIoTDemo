from CollectorNode.OpcUaClient import OpcUaClient, OpcUaConfig
from BaseNode.Server import ServerBase
from CollectorNode.OpcUaClient.opc_ua_client import OpcUaClientFactory
from Common.Communication import CommandModel, ResponseModel, ResponseFactory
from Common.Model import ServerOutline


class OpcUaManagingServer(ServerBase):

    def get_outline(self) -> ServerOutline:
        outline: ServerOutline = ServerOutline(
            name=self.name,
            port=self.port,
            sensor_data_receiver=False,
            sensor_data_sender=True
        )

        return outline

    @property
    def is_online(self):
        return self._active

    def __init__(self):
        super().__init__("OpcUaManager", 8001)
        self._clients: list[OpcUaClient] = []

    async def shutdown(self):
        for client in self._clients:
            if client.is_connected():
                await client.disconnect()

    def on_new_data(self, dataset):
        pass

    def _configure_opc_ua_connection(self, dataset: OpcUaConfig) -> ResponseModel:
        client: OpcUaClient = OpcUaClientFactory.new(dataset)
        if client is not None:
            self._clients.append(client)
            return ResponseFactory.ok()

        return ResponseFactory.nok("Was not able to create client.")

    def _get_configs(self) -> ResponseModel:
        configs = [x.config for x in self._clients]
        return ResponseFactory.ok(values=configs)
