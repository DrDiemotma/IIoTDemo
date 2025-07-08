from fastapi import FastAPI

from BaseNode.Server import ControlServer
from routes import router

control_server = ControlServer()


app = FastAPI()
app.include_router(router)
app.state.control_server = control_server

