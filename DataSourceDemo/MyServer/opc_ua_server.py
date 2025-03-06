from time import sleep

import asyncua
import asyncio
import random
from asyncua import ua

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
                 temperature_name: str = TEMPERATURE,
                 pressure_name: str = PRESSURE,
                 temperature_start_value: float = TEMPERATURE_START_VALUE,
                 pressure_start_value: float = PRESSURE_START_VALUE):
        """
        ctor.
        :param freq: Frequency control, distance between two samples.
        :param port: Port for OPC UA server.
        :param server_endpoint: Definition for the server endpoint.
        :param uri:
        :param device_name:
        :param temperature_name:
        :param pressure_name:
        :param temperature_start_value:
        :param pressure_start_value:
        """
        self._freq = freq
        self._stop = True
        self._current_temperature: float = temperature_start_value
        self._current_pressure: float = pressure_start_value
        self._task: asyncio.Task | None = None

        end_point: str = OPC_TCP \
                            + "://" + IP_ADDRESS \
                            + ":" + str(port) \
                            + "/" + server_endpoint + "/"

        self._server: asyncua.Server = asyncua.Server()
        self._temperature: asyncua.Node | None = None
        self._pressure: asyncua.Node | None = None

        asyncio.run(self._setup_server(uri, end_point, device_name, temperature_name, temperature_start_value,
                                       pressure_name, pressure_start_value))

    def alive_status(self) -> str:
        if self._stop:
            return "Server stopped."
        asyncio.run(self._update_values())
        return f"Server alive, temp: {self._current_temperature}, press: {self._current_pressure}."


    async def _setup_server(self, uri: str, end_point: str, device_name: str,
                            temperature_name: str, temperature_start_value: float,
                            pressure_name: str, pressure_start_value: float):
        await self._server.init()
        self._server.set_endpoint(end_point)
        self._server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        idx: int = await self._server.register_namespace(uri)

        objects: asyncua.Node = self._server.get_objects_node()
        device: asyncua.Node = await objects.add_object(idx, device_name)
        self._temperature: asyncua.Node = await device.add_variable(idx, temperature_name, temperature_start_value)
        self._pressure: asyncua.Node = await device.add_variable(idx, pressure_name, pressure_start_value)
        await self._temperature.set_writable()
        await self._pressure.set_writable()

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
