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
        self._subscriptions: list[Subscription] = []
        self._handles: dict[Subscription, list[int]] = dict()


    async def is_connected(self):
        if self._client is None:
            return False
        try:
            await self._client.check_connection()
        except Exception as e:
            print(f"Not connected: {e}")
            return False
        return True


    async def connect(self, period: int = 50):
        if self._client is None:
            self._client = asyncua.Client(url=self.config.get_url())

        try:
            async with self._client:
                for sub in self.config.subscriptions:
                    idx = await self._client.get_namespace_index(uri=sub.namespace)
                    subscription = await self._client.create_subscription(period, self._handler)
                    self._subscriptions.append(subscription)
                    # todo get the values
                    # time_node: asyncua.Node = self._client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime)
                    value_node: asyncua.Node = await self._client.nodes.objects.get_child([f"{idx}:{sub.object_name}", f"{idx}:{sub.value_name}"])
                    handle = await subscription.subscribe_data_change(value_node)
                    if subscription not in self._handles:
                        self._handles[subscription] = []
                    self._handles[subscription].append(handle)
        except ConnectionRefusedError as cre:
            print(f"Connection was refused: {repr(cre)}")
            return
        except ValueError as value_error:
            print(f"Cannot subscribe: {repr(value_error)}")

    def disconnect(self):
        if len(self._subscriptions) == 0:
            return
        for subscription, handle_list in self._handles.items():
            for handle in handle_list:
                subscription.unsubscribe(handle)

    @property
    def handler(self) -> SubHandler:
        """Getting the handler for data transfer."""
        if self._handler is None:
            self._handler = SubHandler()
        return self._handler


class OpcUaClientFactory:
    @staticmethod
    def new(config_input: OpcUaConfig | str) -> None | OpcUaClient:
        """
        Create a new config or load from hard drive.
        :param config_input: Either a configuration if this is a direct creation or a path to the file which stores the
        configuration.
        :return: OpcUaConfig if it can be created from the input or None.
        """
        config: OpcUaConfig | None = None
        if isinstance(config_input, OpcUaConfig):
            config = config_input
        elif isinstance(config_input, str):
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

    @staticmethod
    def _parse_config_file(config_file: str) -> None | OpcUaConfig:
        try:
            with open(config_file, "r") as f:
                d = json.load(f)
            config = OpcUaConfig(**d)
            return config
        except:
            return None



