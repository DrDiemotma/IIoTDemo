from collections.abc import Callable
from typing import Any

import asyncua
import asyncio

class Poller:
    def __init__(self, node: asyncua.Node, polling_rate: int, publish_callback: Callable[[Any], Any]):
        self._node: asyncua.Node = node
        self._publish_callback = publish_callback
        self._sleep: float = polling_rate / 1000.0
        self._running: bool = False
        self._task: asyncio.Task | None = None

    def start(self):
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._poll())

    def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = None

    async def _poll(self):
        try:
            while self._running:
                value = await self._node.read_value()
                self._publish_callback(value)
                await asyncio.sleep(self._sleep)
        except asyncio.CancelledError:
            print("Cancellation was requested.")
        except Exception:
            raise
