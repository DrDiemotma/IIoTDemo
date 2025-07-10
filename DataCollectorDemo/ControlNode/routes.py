from fastapi import APIRouter, Request

from Common.Communication import ResponseFactory, Response
from ControlNode.Server import ControlServer

router: APIRouter = APIRouter()

@router.get("/is_online", response_model=Response)
def is_online(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/server_namespace", response_model=Response)
def server_namespace(request: Request):
    service: ControlServer = request.app.state.control_server
    response = service.server_namespace
    return ResponseFactory.ok(values=response)

@router.get("/call", response_model=Response)
def call():
    return ResponseFactory.ok(values=str(__file__))
