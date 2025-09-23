import logging
from collections.abc import Callable
from typing import Any
from Common.Communication import DataMessageModel
from datetime import datetime

import asyncua
import asyncio

class Poller:
    """Polling for OPC UA nodes. In a fixed interval, the poller gets data from the node and publishes it on the callback."""
    def __init__(self, node: asyncua.Node,
                 name: str,
                 polling_rate: int,
                 publish_callback: Callable[[DataMessageModel], Any],
                 identifier: int | None = None):
        """
        ctor.
        :param node: Node to observe.
        :param name: Name of the observed value.
        :param polling_rate: How often the data is taken from the
        :param publish_callback:
        """
        logging.info(f"Initializing poller \"{name}\": polling rate {polling_rate}.")
        self._node: asyncua.Node = node
        self._name: str = name
        self._publish_callback = publish_callback
        self._sleep: float = polling_rate / 1000.0
        self._running: bool = False
        self._task: asyncio.Task | None = None
        self._identifier: int | None = identifier

    def start(self):
        """Start the poller. Does nothing if already running."""
        if self._running:
            logging.warning(f"Tried to start the poller for {self._name} while it was already running.")
            return

        self._running = True
        self._task = asyncio.create_task(self._poll())
        logging.info(f"Poller for {self._name} started.")

    async def stop(self):
        """Stop the poller."""
        self._running = False
        logging.info(f"Poller for {self._name} stopping.")

        await asyncio.sleep(1.1 * self._sleep)

        if self._task and not self._task.done():
            self._task.cancel()
        self._task = None
        logging.info(f"Poller for {self._name} stopped.")

    @property
    def running(self) -> bool:
        """Whether the poller is running"""
        return self._running

    async def _poll(self):
        try:
            while self._running:
                value = await self._read_node()
                self._publish_callback(value)
                await asyncio.sleep(self._sleep)
        except asyncio.CancelledError:
            print("Cancellation was requested.")
        except Exception:
            raise

    async def _read_node(self) -> DataMessageModel:
        data_value = await self._node.read_data_value()
        source_timestamp: datetime = data_value.SourceTimestamp
        server_timestamp: datetime = data_value.ServerTimestamp
        value = data_value.Value.Value
        logging.debug(f"Value read from {self._name}: {source_timestamp}/{server_timestamp}: {value}")

        message = DataMessageModel(name=self._name,
                                   timestamp=source_timestamp,
                                   value=value,
                                   server_timestamp=server_timestamp,
                                   identifier=self._identifier)
        return message
