import logging
import os.path
import json

from asyncua.common.subscription import Subscription
from asyncua.ua import UaStatusCodeError

from .opc_ua_config import NodeConfig
from .opc_ua_config import OpcUaConfig
from .sub_handler import SubHandler
from .poller import Poller

import asyncua

class OpcUaClient:
    def __init__(self, name: str):
        """
        ctor
        :param name: Name of the client.
        """
        self.config: OpcUaConfig | None = None
        self._client: asyncua.Client | None = None
        self._handler: SubHandler | None = None
        self._subscriptions: list[Subscription] = []
        self._pollers: list[Poller] = []
        self._handles: dict[Subscription, list[int]] = dict()
        self._name = name
        logging.info(f"Client {name} created.")

    async def is_connected(self):
        if self._client is None:
            logging.info("Client not connected.")
            return False
        try:
            await self._client.check_connection()
        except Exception as e:
            logging.warning(f"Not connected: {e}")
            return False
        return True

    async def connect(self, period: int = 50, use_polling: bool = True):
        """
        Connect to the server.
        :param period: Update frequency.
        :param use_polling: if True: uses polling instead of subscriptions. Use subscriptions if the server supports that only.
        :return: None.
        """
        logging.info(f"Connecting OPC UA client, use polling: {use_polling}")
        if use_polling:
            await self._connect_polling(period)
        await self._connect_subscription(period)

    async def _connect_polling(self, period: int):
        if self._client is None:
            logging.info("Create new OPC UA client (poller).")
            self._client = asyncua.Client(url=self.config.get_url())
        try:
            async with self._client:
                for sub in self.config.subscriptions:
                    value_node: asyncua.Node = await self._get_node(sub)
                    poller: Poller = Poller(value_node, self.name, period, lambda x: None)
                    poller.start()
                    self._pollers.append(poller)
        except Exception as e:
            logging.error(f"Exception caught while creating poller: {e}.")
            raise e


    async def _connect_subscription(self, period: int):
        if self._client is None:
            logging.info("Create new OPC UA client (subscription).")
            self._client = asyncua.Client(url=self.config.get_url())
        try:
            async with self._client:
                for sub in self.config.subscriptions:
                    value_node: asyncua.Node = await self._get_node(sub)
                    handler = self.handler
                    subscription = await self._client.create_subscription(period, handler)
                    self._subscriptions.append(subscription)
                    handle = await subscription.subscribe_data_change(value_node)
                    if subscription not in self._handles:
                        self._handles[subscription] = []
                    self._handles[subscription].append(handle)
        except ConnectionRefusedError as cre:
            logging.error(f"Connection was refused: {repr(cre)}")
            return
        except ValueError as value_error:
            logging.error(f"Cannot subscribe: {repr(value_error)}")
        except UaStatusCodeError as usce:
            logging.error(f"Status code error: {repr(usce)}")
            raise usce

    async def disconnect(self):
        logging.info("Disconnect called.")
        if len(self._subscriptions) == 0 and len(self._pollers) == 0:
            logging.info("No subscriptions or pollers.")
            return
        for subscription, handle_list in self._handles.items():
            for handle in handle_list:
                await subscription.unsubscribe(handle)
        for poller in self._pollers:
            if poller.running:
                await poller.stop()

        self._handles = []
        self._subscriptions = []

    @property
    def handler(self) -> SubHandler:
        """Getting the handler for data transfer."""
        if self._handler is None:
            self._handler = SubHandler()
        return self._handler

    async def _get_node(self, node_config: NodeConfig) -> asyncua.Node | None:
        if not self._client:
            return None
        idx = await self._client.get_namespace_index(uri=node_config.namespace)
        node_str: str = f"ns={idx};s={node_config.object_name}.{node_config.value_name}"
        value_node: asyncua.Node = self._client.get_node(node_str)
        return value_node

    @property
    def name(self) -> str:
        """Name of the OPC UA client."""
        return self._name


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





