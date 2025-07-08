from fastapi import APIRouter, Request

from BaseNode.Server import ControlServer

router = APIRouter()

@router.get("/is_online")
def is_online(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.is_online
    return response

@router.get("/server_namespace")
def server_namespace(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.server_namespace
    return response

