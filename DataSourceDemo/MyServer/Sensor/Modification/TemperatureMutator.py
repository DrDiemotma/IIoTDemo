import random
from datetime import datetime

from MyServer.Sensor import TemperatureSensor
from MyServer.Sensor.Modification.mutator import  Mutator, MutatorFactory, Mode, State


class TemperatureMutator(Mutator[float]):
    """Simulator implementation for temperature sensors."""

    def __init__(self, sensor: TemperatureSensor, start_value: float = 20.0, random_seed: int = 42, st_dev: float = 0.5,
                 value_idle: float = 20.0, value_running: float = 80.0, value_running_broken: float = 120.0,
                 adaption_rate: float = 0.05):
        """
        ctor.
        :param sensor: Sensor to mutate.
        :param start_value: Start value of the sensor.
        :param random_seed: Random generator seed for the noise.
        :param st_dev: Standard deviation of the measurements.
        :param value_idle: Target value when is the machine is idle.
        :param value_running: Target value when the machine is running, but healthy.
        :param value_running_broken: Target value when the machine is running, but broken.
        :param adaption_rate: How fast the system reacts to other states.
        """
        super().__init__(sensor, start_value)
        self.__random = random.Random(random_seed)
        self.__st_dev: float = st_dev
        self._value_idle: float = value_idle
        self._value_running: float = value_running
        self._value_running_broken: float = value_running_broken
        self._adaption_rate = adaption_rate
        self._last_measurement: datetime = datetime.now()


    def _update_current_value(self) -> tuple[datetime, float]:
        target_value = self._target_value()
        time_stamp = datetime.now()
        return time_stamp, target_value

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
        raise NotImplementedError("To be implemented")




class TemperatureMutatorFactory(MutatorFactory[float]):

    @staticmethod
    def from_dict(d: dict) -> TemperatureMutator:
        return TemperatureMutator(**d)
