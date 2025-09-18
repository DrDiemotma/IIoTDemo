from fastapi import APIRouter, Request

from MyServer import OpcUaTestServer
from MyServer.Lifetime import MachineModelBase
from MyServer.MachineOperation import SensorConfig, SensorConfigList, SensorId
from MyServer.MachineOperation import SensorType
from MyServer.Sensor import TemperatureSensor, SensorBase
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
    def to_sensor_config(s: SensorBase) -> SensorConfig:
        dictionary = s.to_dict()
        config: SensorConfig = SensorConfig(
            type=dictionary["type"],
            identifier=s.identifier,
            simulator_config=None
        )
        return config

    server: OpcUaTestServer = request.app.state.server
    sensors: list[SensorBase] = server.model.sensors
    config_list = SensorConfigList(sensors=[to_sensor_config(x) for x in sensors])
    return config_list

@router.post("/delete_sensor")
async def delete_sensor(sensor_id: SensorId, request: Request):
    server: OpcUaTestServer = request.app.state.server
    sensor = next((x for x in server.model.sensors if x.sensor_type == sensor_id.type and x.identifier == sensor_id.identifier), None)
    if sensor is None:
        return False

    server.model.delete_sensor(sensor_id)
    return True

@router.post("/start")
async def start(request: Request):
    server: OpcUaTestServer = request.app.state.server
    await server.start()

@router.post("/stop")
async def stop(request: Request):
    server: OpcUaTestServer = request.app.state.server
    await server.stop()

@router.get("/is_running")
async def is_running(request: Request):
    server: OpcUaTestServer = request.app.state.server
    result = server.alive_status()
    return result

@router.post("/start_job")
async def start_job(request: Request):
    server: OpcUaTestServer = request.app.state.server
    started = await server.start_job()
    return started

@router.post("/stop_job")
async def stop_job(request: Request):
    server: OpcUaTestServer = request.app.state.server
    stopped = await server.stop_job()
    return stopped

@router.post("/custom_message")
async def custom_message(message, request: Request):
    server: OpcUaTestServer = request.app.state.server
    model: MachineModelBase = server.model
    model.custom_message(message)
    return
