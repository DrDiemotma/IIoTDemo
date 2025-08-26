from MyServer.Sensor.Modification.TemperatureMutator import TemperatureMutator
from MyServer.Sensor import TemperatureSensor


def test_value_at():
    sensor: TemperatureSensor = TemperatureSensor(1)
    sut: TemperatureMutator = TemperatureMutator(sensor)
    pass