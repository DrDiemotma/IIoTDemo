from fastapi import APIRouter, Request
from Common.Communication import ResponseFactory, ResponseModel, CommandModel
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

@router.post("/register", response_model=ResponseModel)
async def register(data: ServerOutline, request: Request):
    print(f"registering {data.name}")
    service: ControlServer = request.app.state.control_server
    service.register_server(data)
    return ResponseFactory.ok()

@router.post("/publish_command", response_model=ResponseModel)
async def publish_command(command: CommandModel, request: Request):
    service: ControlServer = request.app.state.control_server
    response = await service.publish_command(command)
    return response

@router.get("/get_services", response_model=ResponseModel)
async def get_services(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.get_server_names()
    print(response)
    return ResponseFactory.ok(values=response)

