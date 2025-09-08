import asyncua
import asyncio
import random
import os
from asyncua import ua
from MyServer.Lifetime import MachineModel

OPC_TCP: str = "opc.tcp"
IP_ADDRESS: str = "0.0.0.0"
OPC_UA_PORT: int = 4840
SERVER_ENDPOINT: str = "freeopcua/server"
URI: str = "http://example.org/opcua"
DEVICE: str = "Device"
TEMPERATURE: str = "Temperature"
PRESSURE: str = "Pressure"
FREQ: float = 1.0
TEMPERATURE_START_VALUE: float = 20.0
PRESSURE_START_VALUE: float = 1013.25
CONFIGURATION_FILE: str = "MachineModel.json"

class OpcUaTestServer:
    """
    Test OPC UA server with some simulated values as output.
    """

    def __init__(self,
                 freq: float = FREQ,
                 port: int = OPC_UA_PORT,
                 server_endpoint: str = SERVER_ENDPOINT,
                 uri: str = URI,
                 device_name: str = DEVICE,
                 machine_model_file: str = CONFIGURATION_FILE):
        """
        ctor.
        :param freq: Frequency control, distance between two samples.
        :param port: Port for OPC UA server.
        :param server_endpoint: Definition for the server endpoint.
        :param uri:
        :param device_name:
        :param machine_model_file: File to store the configuration of the machine model.
        """
        self._freq = freq
        self._stop = True
        self._task: asyncio.Task | None = None
        self._uri: str = uri
        self._device_name: str = device_name
        self._machine_model_file = machine_model_file

        self._end_point: str = (OPC_TCP
                                + "://" + IP_ADDRESS
                                + ":" + str(port)
                                + "/" + server_endpoint + "/")

        self._server: asyncua.Server = asyncua.Server()
        self._model: MachineModel = MachineModel()
        if os.path.isfile(machine_model_file):
            self._model.restore_configuration(self._machine_model_file)

    @property
    def model(self) -> MachineModel:
        return self._model


    def alive_status(self) -> str:
        if self._stop:
            return "Server stopped."
        asyncio.create_task(self._update_values())
        return f"Server alive, temp: {self._current_temperature}, press: {self._current_pressure}."


    async def setup_server(self):
        await self._server.init()
        self._server.set_endpoint(self._end_point)
        self._server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        idx: int = await self._server.register_namespace(self._uri)

        objects: asyncua.Node = self._server.get_objects_node()


    async def start(self):
        print("Starting server")
        await self._server.start()
        self._stop = False

        self._task = asyncio.create_task(self._update_values())
        print("Server running.")

    async def stop(self):
        print("Stopping server")
        self._stop = True
        await asyncio.sleep(0.01 + self._freq)
        self._task.cancel()
        self._task = None
        print("Server stopped.")

    async def _update_values(self):
        self._current_temperature = random.gauss(self._current_temperature, 0.02)
        self._current_pressure = random.gauss(self._current_pressure, 15.0)
        await self._temperature.set_value(self._current_temperature)
        await self._pressure.set_value(self._current_pressure)
