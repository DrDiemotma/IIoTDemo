from fastapi import APIRouter, Request

from Common.Communication import ResponseFactory, ResponseModel
from Common.Model import ServerOutline
from ControlNode.Server import ControlServer

router: APIRouter = APIRouter()

@router.get("/", response_model=ResponseModel)
def root_call():
    return ResponseFactory.ok(values="ControlNode")

@router.get("/is_online", response_model=ResponseModel)
def is_online(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/server_namespace", response_model=ResponseModel)
def server_namespace(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.server_namespace
    return ResponseFactory.ok(values=response)

@router.get("/call", response_model=ResponseModel)
def call():
    return ResponseFactory.ok(values=str(__file__))

@router.post("/register", response_model=ResponseModel)
async def register(data: ServerOutline, request: Request):
    print("Start registering")
    service: ControlServer = request.app.state.control_server
    service.register_server(data)
    return ResponseFactory.ok()
