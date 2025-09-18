import json
from typing import Any

from MyServer.Lifetime.machine_model_base import MachineModelBase
from MyServer.MachineOperation.sensor_data_model import SensorId
from MyServer.MachineOperation import State, Mode, SensorType
from MyServer.Sensor import SensorBase, Mutator, TemperatureSensor
from MyServer.Sensor.Modification.TemperatureMutator import TemperatureMutator, TemperatureMutatorFactory
from MyServer.Sensor.Modification.mutator import MutatorFactory

MACHINE_STATE: str = "machine_state"


class MachineModel(MachineModelBase):
    """Model for machine simulation. Handles the machine state and mode."""

    def custom_message(self, message: dict[str, Any]) -> bool:
        d_used = {x: False for x in message.keys()}
        if MACHINE_STATE in message:
            set_state: bool = message[MACHINE_STATE]
            if set_state:
                self.set_state_normal()
                d_used[MACHINE_STATE] = True
            else:
                self.set_state_broken()
                d_used[MACHINE_STATE] = True

        # find any element that has not been processed
        fully_used = all(d_used.values())
        return fully_used




    def start_job(self):
        for mutator in self._mutators:
            mutator.mode = Mode.RUNNING

    def stop_job(self):
        for mutator in self._mutators:
            mutator.mode = Mode.IDLE

    def set_state_broken(self):
        for mutator in self._mutators:
            mutator.state = State.BROKEN

    def set_state_normal(self):
        for mutator in self._mutators:
            mutator.state = State.NORMAL

    def __init__(self):
        self._sensors: list[SensorBase] = []
        self._mutators: list[Mutator] = []
        self._state: State = State.NORMAL
        self._mode: Mode = Mode.RUNNING

        self._sensor_factory_map: dict[SensorType, MutatorFactory] = {
            SensorType.TEMPERATURE: TemperatureMutatorFactory(),
        }

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

    @property
    def mutators(self) -> list[Mutator]:
        """Get a list of current mutators to fine-tune behaviour."""
        return list(self._mutators)

    @property
    def sensors(self) -> list[SensorBase]:
        """Get the sensors"""
        return [x.sensor for x in self._mutators]


    def save_configuration(self, file_path: str):
        """Save the current configuration to a file."""
        data = [mutator.to_dict() for mutator in self._mutators]
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def restore_configuration(self, file_path: str):
        """Load mutators from a file."""
        with open(file_path, "r") as f:
            dictionary = json.load(f)
        for entry in dictionary:
            sensor_type = SensorType(entry["type"])
            try:
                factory: MutatorFactory = self._sensor_factory_map[sensor_type]
            except KeyError:
                raise NotImplementedError(f"The case {entry['type']} is not implemented yet.")

            mutator: Mutator = factory.from_dict(entry)
            self._sensors.append(mutator.sensor)
            self._mutators.append(mutator)

    def delete_sensor(self, sensor_id: SensorId):
        mutator = next(x for x in self._mutators
                       if x.sensor.sensor_id == sensor_id)
        sensor = mutator.sensor
        sensor.stop()
        self._mutators.remove(mutator)
        self._sensors.remove(sensor)

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
