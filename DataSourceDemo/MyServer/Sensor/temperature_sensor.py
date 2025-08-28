import json

from MyServer.Sensor.sensor_base import SensorBase

class TemperatureSensor(SensorBase[float]):
    """Temperature sensor implementation."""
    def __init__(self,
                 identifier: int,
                 namespace: str = "Sensors",
                 updates_per_second: float = 0.5):
        super().__init__(name=f"Temperature_sensor_{identifier:03d}",
                         namespace=namespace,
                         updates_per_second=updates_per_second)
        self._identifier = identifier

    def to_json(self) -> str:
        d = {
            "identifier": self._identifier,
            "namespace": self.namespace,
            "updates_per_second": self.updates_per_second
        }

        return json.dumps(d)

    def on_polling(self):
        pass  # currently nothing to do here


