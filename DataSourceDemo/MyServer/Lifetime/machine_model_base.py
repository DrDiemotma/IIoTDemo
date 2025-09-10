from abc import ABC, abstractmethod

from MyServer.MachineOperation.sensor_data_model import SensorId
from MyServer.Sensor import SensorBase, Mutator


class MachineModelBase(ABC):
    """Abstract machine model class."""

    @abstractmethod
    def add_sensor(self, sensor: SensorBase, mutator: Mutator = None, **kwargs):
        """Add a sensor to the configuration.
        :param sensor: The sensor to add.
        :param mutator: Optional mutator, for example, to simulate sensor behaviour.
        """
        pass

    @abstractmethod
    def delete_sensor(self, sensor_id: SensorId):
        """Delete a sensor from the configuration.
        :param sensor_id: The id from the sensor.
        """
        pass

    @property
    @abstractmethod
    def sensors(self) -> list[SensorBase]:
        """List of current sensors."""
        pass

    @abstractmethod
    def save_configuration(self, file_path: str):
        """Save the current configuration to a file."""
        pass

    @abstractmethod
    def restore_configuration(self, file_path: str):
        """Restore the configuration from a file."""
        pass