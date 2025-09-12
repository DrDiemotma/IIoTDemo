import pytest

from MyServer import OpcUaTestServer
from MyServer.Lifetime import MachineModelBase
from MyServer.MachineOperation import SensorId
from MyServer.Sensor import TemperatureSensor, SensorBase, Mutator


class MachineModelMock(MachineModelBase):
    _sensors = []
    def restore_configuration(self, file_path: str):
        pass

    def save_configuration(self, file_path: str):
        pass

    @property
    def sensors(self) -> list[SensorBase]:
        return self._sensors

    def delete_sensor(self, sensor_id: SensorId):
        pass

    def add_sensor(self, sensor: SensorBase, mutator: Mutator = None, **kwargs):
        self._sensors.append(sensor)


@pytest.fixture
def opc_ua_server():
    machine_mock = MachineModelMock()
    if len(machine_mock.sensors) == 0:  # just make sure some sensor is populated
        temperature_sensor = TemperatureSensor(1)
        machine_mock.add_sensor(temperature_sensor)

    assert len(machine_mock.sensors) > 0, print("Sensor was not added to the system.")

    yield OpcUaTestServer(machine=machine_mock)

@pytest.mark.asyncio
async def test_setup_server(opc_ua_server: OpcUaTestServer):
    assert await opc_ua_server.setup_server(), print("Server setup not completed.")
    sensors = opc_ua_server.model.sensors
    for sensor in sensors:
        pass
