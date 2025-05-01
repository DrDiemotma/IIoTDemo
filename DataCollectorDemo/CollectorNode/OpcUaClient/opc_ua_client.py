import os.path
import json

from asyncua.common.subscription import Subscription

from .opc_ua_config import OpcUaConfig
from .sub_handler import SubHandler

import asyncua
from asyncua import ua


class OpcUaClient:
    def __init__(self):
        self.config: OpcUaConfig | None = None
        self._client: asyncua.Client | None = None
        self._handler: SubHandler | None = None
        self._subscription: Subscription | None = None


    async def is_connected(self):
        if self._client is None:
            return False
        try:
            await self._client.check_connection()
        except Exception as e:
            print(f"Not connected: {e}")
            return False
        return True


    async def connect(self):
        if self._client is None:
            self._client = asyncua.Client(self.config.get_url())

        self._handler = SubHandler()
        async with self._client:
            idx = await self._client.get_namespace_index(uri=self.config.uri)
            # todo subscribe to the data nodes
            self._subscription = await self._client.create_subscription(500, self._handler)
            node = (self._client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime), )
            await self._subscription.subscribe_data_change(node)

    def disconnect(self):
        if self._subscription is None:
            return
        self._subscription.delete()


class OpcUaClientFactory:
    @staticmethod
    def new(config_input: OpcUaConfig | str) -> None | OpcUaClient:
        config: OpcUaConfig | None = None
        if config_input is OpcUaConfig:
            config = config_input
        elif config_input is str:
            if not os.path.isfile(config_input):
                return None
            config: OpcUaConfig = OpcUaClientFactory._parse_config_file(config_input)
            if config is None:
                return None

        if config is None:
            return None

        client = OpcUaClient()
        client.config = config
        return client

    def start(self):
        pass

    def stop(self):
        pass

    @staticmethod
    def _parse_config_file(config_file: str) -> None | OpcUaConfig:
        try:
            with open(config_file, "r") as f:
                d = json.load(f)
            config = OpcUaConfig(
                ip = d["ip"],
                port = d["port"],
                server_id=d["server_id"],
                uri=d["uri"]
            )
            return config
        except:
            return None



