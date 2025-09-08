from fastapi import APIRouter, Request

from MyServer import OpcUaTestServer
from MyServer.MachineOperation.sensor_data_model import SensorConfig, SensorConfigList, SensorId
from MyServer.MachineOperation import SensorType
from MyServer.Sensor import TemperatureSensor, Mutator
from MyServer.Sensor.Modification.TemperatureMutator import TemperatureMutator

router: APIRouter = APIRouter()

@router.post("/add_sensor")
async def add_sensor(sensor_config: SensorConfig, request: Request):

    server: OpcUaTestServer = request.app.state.server
    match sensor_config.type:
        case SensorType.TEMPERATURE:
            temperature_sensor: TemperatureSensor = TemperatureSensor(sensor_config.identifier)
            if not sensor_config.simulator_config is None:
                temperature_mutator: TemperatureMutator = TemperatureMutator(temperature_sensor, **sensor_config.simulator_config)
                server.model.add_sensor(temperature_sensor, temperature_mutator)
            else:
                server.model.add_sensor(temperature_sensor)
            return True

    return False


@router.get("/get_sensors", response_model=SensorConfigList)
async def get_sensors(request: Request):
    def to_sensor_config(m: Mutator) -> SensorConfig:
        dictionary = m.to_dict()
        config: SensorConfig = SensorConfig(
            type=dictionary["type"],
            identifier=m.sensor.identifier,
            simulator_config=dictionary
        )
        return config

    server: OpcUaTestServer = request.app.state.server
    mutators: list[Mutator] = server.model.mutators
    config_list = SensorConfigList(sensors=[to_sensor_config(x) for x in mutators])
    return config_list

@router.post("/delete_sensor")
async def delete_sensor(sensor_id: SensorId, request: Request):
    server: OpcUaTestServer = request.app.state.server
    sensor = next((x.sensor for x in server.model.mutators if x.sensor.sensor_type == sensor_id.type and x.sensor.identifier == sensor_id.identifier), None)
    if sensor is None:
        return False

    server.model.delete_sensor(sensor_id)
    return True


