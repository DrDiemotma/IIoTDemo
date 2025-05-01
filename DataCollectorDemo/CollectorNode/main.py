from fastapi import FastAPI
from Common.Communication import Command

from Server.control_server import ControlServer
from OpcUaClient import OpcUaManagingServer
from UiServer import UiServer




if __name__ == "__main__":
    app = FastAPI()
    server = ControlServer()
    ui_server = UiServer()
    opcua_server = OpcUaManagingServer()
    server.register_server(ui_server)
    server.register_server(opcua_server)

    @app.post("/" + server.server_namespace)
    def call_control_server(cmd: Command):
        server.execute_command(cmd)


