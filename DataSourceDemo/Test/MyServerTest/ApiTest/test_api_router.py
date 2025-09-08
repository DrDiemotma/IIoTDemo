from fastapi.testclient import TestClient

from MyServer.MachineOperation.sensor_data_model import SensorId
from main import app

from MyServer.Api import SensorConfig
from MyServer.MachineOperation import SensorType

def create_test_client() -> TestClient:
    client = TestClient(app)
    return client


def test_add_sensor_simulator_config_none():
    sensor_config: SensorConfig = SensorConfig(type=SensorType.TEMPERATURE, identifier=42, simulator_config=None)
    client: TestClient = create_test_client()
    response = client.post("/add_sensor", json=sensor_config.model_dump())
    assert response.is_success, print(response)

def test_get_sensors():
    sensor_config: SensorConfig = SensorConfig(type=SensorType.TEMPERATURE, identifier=42, simulator_config=None)
    client: TestClient = create_test_client()
    response = client.post("/add_sensor", json=sensor_config.model_dump())
    assert response.is_success, print(response)

    response = client.get("/get_sensors")
    assert response.is_success
    data = response.json()
    assert "sensors" in data, print(f"Response model must include \"sensors\".")
    assert len(data["sensors"]) > 0, print("Sensors must not be empty.")

def test_delete_sensor():
    sensor_config: SensorConfig = SensorConfig(type=SensorType.TEMPERATURE, identifier=42, simulator_config=None)
    client: TestClient = create_test_client()
    response = client.post("/add_sensor", json=sensor_config.model_dump())
    assert response.is_success, print(response)

    sensor_id = SensorId(
        identifier=sensor_config.identifier,
        type=sensor_config.type
    )

    response = client.post("/delete_sensor", json=sensor_id.model_dump())
    assert response.is_success, print(response)

    response = client.get("/get_sensors")
    assert response.is_success, print(response)
    assert len(response.json()["sensors"]) == 0, print("Sensor was not deleted.")


