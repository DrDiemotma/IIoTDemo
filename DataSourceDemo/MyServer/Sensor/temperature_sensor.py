from datetime import datetime

from MyServer.Sensor.sensor_base import SensorBase

class TemperatureSensor(SensorBase[float]):
    def on_polling(self):
        pass

    def __init__(self,
                 identifier: int,
                 namespace: str = "Sensors",
                 updates_per_second: float = 0.5):
        super().__init__(name=f"Temperature_sensor_{identifier:03d}",
                         namespace=namespace,
                         updates_per_second=updates_per_second)


    def to_json(self):
        pass


