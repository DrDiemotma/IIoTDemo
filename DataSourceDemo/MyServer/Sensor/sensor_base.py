from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime, timedelta
import asyncio
from decimal import InvalidOperation


class SensorBase[T](ABC):
    """
    Base class for sensor types.
    """
    __namespace: str
    __name: str
    __updates_per_second: float
    __callbacks: list[Callable[[datetime, T], ...]]
    __callback_locks: dict[Callable[[datetime, T], ...], asyncio.Lock]
    __last_value: T
    __last_measured_time: datetime
    __source: Callable[[...], T] | None
    __task: asyncio.Task | None

    def __init__(self, name: str, namespace: str, updates_per_second: float):
        """
        ctor.
        :param name: Name of the sensor.
        :param namespace: Namespace of the sensor (where in the data model to be present).
        :param updates_per_second: How often the sensor is updated.
        """
        self.__name = name
        self.__namespace = namespace
        self.__callbacks: list[Callable[[datetime, T], ...]] = []
        self.__updates_per_second = updates_per_second
        self.__callback_locks: dict[Callable[[datetime, T], ...], asyncio.Lock] = {}
        self.__source = None
        self.__task = None

    def __del__(self):
        self.stop()


    @property
    def namespace(self) -> str:
        """The namespace of the sensor, that is, its location in the data model."""
        return self.__namespace

    @property
    def name(self) -> str:
        """The name of the sensor."""
        return self.__name

    @property
    def updates_per_second(self):
        """The updates per second."""
        return self.__updates_per_second

    def last_value(self) -> tuple[datetime, T]:
        return self.__last_measured_time, self.__last_value

    @abstractmethod
    def to_json(self) -> str:
        """Create a JSON string from which the sensor can be reconstructed (but the recorded data)."""
        pass

    @abstractmethod
    def on_polling(self):
        """Is called when data is polled. Used for logging or similar actions."""
        pass

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value: Callable[[...], T]):
        if self.__task is not None:
            return
        self.__source = value

    @property
    def running(self):
        return self.__task is not None

    async def __poller(self):
        time_span: float = 1.0 / self.__updates_per_second
        while self.__source is not None:
            start_time: datetime = datetime.now()  # start of the full process
            self.on_polling()
            value: T = self.source()
            time: datetime = datetime.now()  # time when received - source might take a while
            await self.on_new_data(time, value)
            stop_time: datetime = datetime.now()  # awaited new data received
            time_delta: float = (stop_time - start_time).total_seconds()
            if time_delta < time_span:
                await asyncio.sleep(time_span - time_delta)

    def start(self):
        if self.__task is not None:
            raise InvalidOperation("Task already started.")
        if self.__source is None:
            return

        self.__task = asyncio.create_task(self.__poller())

    def stop(self):
        if self.__task is None:
            return
        if not self.__task.done():
            self.__task.cancel()
        self.__task = None



    async def on_new_data(self, timestamp: datetime, data: T):
        """
        To be called on new recorded data.
        :param timestamp: The recording time of the measurement.
        :param data: Recorded data.
        """
        self.__last_value = data
        self.__last_measured_time = timestamp

        # avoids potential race conditions if called again before the callback has returned
        async def safe_call(cb: Callable[[datetime, T], ...]):
            lock = self.__callback_locks.setdefault(cb, asyncio.Lock())
            async with lock:
                await cb(timestamp, data)

        try:
            await asyncio.gather(*(safe_call(cb) for cb in self.__callbacks))
        except:
            raise

    def add_callback(self, callback: Callable[[datetime, T], ...]):
        """Add a callback. Can be added only once.
        :param callback: The callback to add.
        """
        if callback not in self.__callbacks:
            self.__callbacks.append(callback)

    def remove_callback(self, callback: Callable[[datetime, T], ...]) -> bool:
        """
        Remove a callback from the registered list.
        :param callback: The callback to be removed.
        :return: Whether the callback was removed.
        """
        if callback not in self.__callbacks:
            return False

        self.__callbacks.remove(callback)
        return True
