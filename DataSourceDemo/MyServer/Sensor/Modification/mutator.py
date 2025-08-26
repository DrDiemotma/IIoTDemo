from datetime import datetime
from MyServer.MachineOperation import State, Mode
from abc import ABC, abstractmethod


class Mutator[T](ABC):
    """
    Mutator class for data, depending on state and operation mode of the machine.
    """
    def __init__(self, start_value: T, mode: Mode = Mode.IDLE, state: State = State.NORMAL):
        self.__current_value: T = start_value
        self.__last_measurement: datetime = datetime.now()
        self.__mode: Mode = mode
        self.__state: State = state

    @property
    def mode(self) -> Mode:
        """Get the currently set mode."""
        return self.__mode

    @mode.setter
    def mode(self, mode: Mode):
        """Set the mode."""
        self.__mode = mode

    @property
    def state(self):
        """Get the state of the machine."""
        return self.__state

    @state.setter
    def state(self, state: State):
        """Set the state."""
        self.__state = state

    @abstractmethod
    def to_dict(self) -> dict:
        """Translate the data to a serializable json."""
        pass

    @abstractmethod
    def _update_current_value(self) -> tuple[datetime, T]:
        """Update the current value."""
        pass

    def measure(self) -> T:
        self.__current_value = self._update_current_value()



class MutatorFactory[T](ABC):
    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> Mutator[T]:
        """create a new instance from a dict."""