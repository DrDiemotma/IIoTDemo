from fastapi import FastAPI
from ControlNode.routes import router
from ControlNode.Server import ControlServer

print("Creating app...")
app: FastAPI = FastAPI()
print("Setting up server.")
control_server: ControlServer = ControlServer()
print("Configure app")
app.state.control_server = control_server
app.include_router(router)
print("Setup done")
