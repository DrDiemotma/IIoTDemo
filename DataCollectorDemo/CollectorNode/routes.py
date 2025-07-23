from fastapi import APIRouter, Request

from CollectorNode.OpcUaClient import OpcUaManagingServer
from Common.Communication import ResponseFactory, ResponseModel

router: APIRouter = APIRouter()

@router.get("/", response_model=ResponseModel)
def root_call():
    return ResponseFactory.ok(values="CollectorNode")

@router.get("/is_online", response_model=ResponseModel)
def is_online(request: Request):
    service: OpcUaManagingServer = request.app.state.opc_ua_managing_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/server_namespace", response_model=ResponseModel)
def server_namespace(request: Request):
    service: OpcUaManagingServer = request.app.opc_ua_managing_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

@router.get("/call", response_model=ResponseModel)
def call():
    return ResponseFactory.ok(values=str(__file__))


