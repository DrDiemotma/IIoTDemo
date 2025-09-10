import pytest

from MyServer import OpcUaTestServer
from MyServer.Lifetime import MachineModel
from MyServer.Sensor import TemperatureSensor


@pytest.fixture
def opc_ua_server():
    yield OpcUaTestServer()

def test_setup_server(opc_ua_server: OpcUaTestServer):
    model: MachineModel = opc_ua_server.model
    assert model is not None, print("Server is not fully initialized.")
    if len(model.mutators) == 0:  # just make sure some sensor is populated
        temperature_sensor = TemperatureSensor(1)
        model.add_sensor(temperature_sensor)

    assert len(model.mutators) > 0, print("Sensor was not added to the system.")

    pass