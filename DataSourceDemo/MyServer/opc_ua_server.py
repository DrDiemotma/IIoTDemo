import json

import asyncua
import asyncio
import os
from asyncua import ua
from MyServer.Lifetime import MachineModel
from MyServer.Lifetime.machine_model_base import MachineModelBase
from MyServer.OpcUa.server_configuration import ServerConfiguration

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
                 server_endpoint: str = SERVER_ENDPOINT,
                 server_configuration: ServerConfiguration | None = None,
                 machine_model_file: str = CONFIGURATION_FILE,
                 machine: MachineModelBase | None = None):
        """
        ctor.
        :param freq: Frequency control, distance between two samples. Used for clean shutdowns.
        :param server_endpoint: Definition for the server endpoint.
        :param server_configuration: Configuration for the server.
        :param machine_model_file: File to store the configuration of the machine model.
        :param machine: Machine representation.
        """
        self._freq = freq
        self._stopped = True
        self._task: asyncio.Task | None = None
        self._configuration: ServerConfiguration = server_configuration
        self._machine_model_file = machine_model_file
        self._set_up: bool = False

        self._end_point: str = (OPC_TCP
                                + "://" + IP_ADDRESS
                                + ":" + str(self._configuration.port)
                                + "/" + server_endpoint + "/")

        self._server: asyncua.Server = asyncua.Server()
        self._model: MachineModelBase = machine if machine is not None else MachineModel()
        if os.path.isfile(machine_model_file):
            self._model.restore_configuration(self._machine_model_file)

    @property
    def model(self) -> MachineModelBase:
        return self._model

    def alive_status(self) -> str:
        pass

    async def setup_server(self) -> bool:
        if not self._set_up and not self._stopped:
            return False

        await self._server.init()
        self._server.set_endpoint(self._end_point)
        self._server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        # todo the sensor must be installed in an OPC UA object
        return True


    async def start(self):
        print("Starting server")
        await self._server.start()
        self._stopped = False


    async def stop(self):
        print("Stopping server")
        self._stopped = True
        await asyncio.sleep(0.01 + self._freq)
        self._task.cancel()
        self._task = None
        print("Server stopped.")


    def save_configuration(self, file_name: str):
        """
        Save the current configuration to a file.
        :param file_name: The file name to save the configuration to. Notice that it will be overwritten.
        """
        if not self._set_up:
            # configurations that are not set up don't need to be saved.
            return

        if os.path.isfile(file_name):
            os.remove(file_name)

        with open(file_name, "w") as f:
            json.dump(self._configuration, f)
