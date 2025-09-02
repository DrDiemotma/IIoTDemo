import json

from MyServer.MachineOperation import State, Mode, SensorType
from MyServer.Sensor import SensorBase, Mutator, TemperatureSensor
from MyServer.Sensor.Modification.TemperatureMutator import TemperatureMutator, TemperatureMutatorFactory


class MachineModel:
    """Model for machine simulation. Handles the machine state and mode."""
    def __init__(self):
        self._sensors: list[SensorBase] = []
        self._mutators: list[Mutator] = []
        self._state: State = State.NORMAL
        self._mode: Mode = Mode.RUNNING

    def __del__(self):
        for sensor in self._sensors:
            sensor.stop()

    def add_sensor(self, sensor: SensorBase, mutator: Mutator = None, **kwargs):
        """
        Add a sensor.
        :param sensor: Sensor to add.
        :param mutator: mutator for the sensor. If None, a default mutator is created for the respective sensor.
        """
        self._sensors.append(sensor)
        if mutator is not None:
            mutator.state = self._state
            mutator.mode = self._mode
            self._mutators.append(mutator)
            return

        # create the mutator automatically
        if isinstance(sensor, TemperatureSensor):
            temperature_mutator: TemperatureMutator =  TemperatureMutator(sensor, **kwargs)
            temperature_mutator.state = self._state
            temperature_mutator.mode = self._mode
            self._mutators.append(temperature_mutator)

    def get_mutators(self) -> list[Mutator]:
        """Get the list of current mutators to fine-tune behaviour."""
        return self._mutators

    def save_configuration(self, file_path: str):
        data = [mutator.to_dict() for mutator in self._mutators]
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def restore_configuration(self, file_path: str):
        with open(file_path, "r") as f:
            dictionary = json.load(f)
        for entry in dictionary:
            sensor_type = SensorType(entry["type"])
            match sensor_type:
                case SensorType.TEMPERATURE:
                    mutator: TemperatureMutator = TemperatureMutatorFactory.from_dict(entry)
                    self._sensors.append(mutator.sensor)
                    self._mutators.append(mutator)
                case _:
                    raise NotImplementedError(f"The case {entry["type"]} is not implemented yet.")


    @property
    def state(self) -> State:
        """Get the current state of the machine."""
        return self._state

    @state.setter
    def state(self, value: State):
        """Set the current state of the machine."""
        for m in self._mutators:
            m.state = value

        self._state = value

    @property
    def mode(self) -> Mode:
        """Get the current mode of the machine."""
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        """Set the current mode of the machine."""
        for m in self._mutators:
            m.mode = value

        self._mode = value
