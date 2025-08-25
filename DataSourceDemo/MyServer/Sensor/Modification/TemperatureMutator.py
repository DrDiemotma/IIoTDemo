import random
from datetime import datetime

from MyServer.Sensor import TemperatureSensor
from MyServer.Sensor.Modification.mutator import  Mutator, MutatorFactory, Mode, State


class TemperatureMutator(Mutator[float]):

    def __init__(self, start_value: float = 20.0, random_seed: int = 42, st_dev: float = 0.5,
                 value_idle: float = 20.0, value_running: float = 80.0, value_running_broken: float = 120.0):
        super().__init__(start_value)
        self.__random = random.Random(random_seed)
        self.__st_dev: float = st_dev
        self._value_idle: float = value_idle
        self._value_running: float = value_running
        self._value_running_broken: float = value_running_broken
        self._last_measurement: datetime = datetime.now()


    def _update_current_value(self, timestamp: datetime) -> float:
        last_value: float = self.current_value
        last_measurement: datetime = self._last_measurement
        time_delta = timestamp - last_measurement
        target_value:float = self._target_value()

        return last_value

    def _target_value(self) -> float:
        match self.state:
            case State.NORMAL:
                return self._target_value_healthy()
            case State.BROKEN:
                return self._target_value_broken()
        return 0

    def _target_value_healthy(self) -> float:
        match self.mode:
            case Mode.IDLE:
                return self._value_idle
            case Mode.RUNNING:
                return self._value_running

    def _target_value_broken(self) -> float:
        match self.mode:
            case Mode.IDLE:
                return self._value_idle
            case Mode.RUNNING:
                return self._value_running_broken

    def to_dict(self) -> dict:
        pass


class TemperatureMutatorFactory(MutatorFactory[float]):

    @staticmethod
    def from_dict(d: dict) -> TemperatureMutator:
        return TemperatureMutator(**d)
