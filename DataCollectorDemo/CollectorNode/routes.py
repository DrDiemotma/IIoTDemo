from fastapi import APIRouter, Request

from CollectorNode.OpcUaClient import OpcUaManagingServer
from Common.Communication import ResponseFactory, Response

router: APIRouter = APIRouter()

@router.get("/is_online")
def is_online(request: Request, response_model=Response):
    service: OpcUaManagingServer = request.app.state.opc_ua_managing_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/server_namespace")
def server_namespace(request: Request, response_model=Response):
    service: OpcUaManagingServer = request.app.opc_ua_managing_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/call", response_model=Response)
def call():
    return ResponseFactory.ok(values=str(__file__))
