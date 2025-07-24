from fastapi import APIRouter, Request

from UiNode.UiServer import UiServer
from Common.Communication import ResponseFactory, ResponseModel

router: APIRouter = APIRouter()

@router.get("/", response_model=ResponseModel)
def root_call():
    return ResponseFactory.ok(values="UiServer")

@router.get("/is_online", response_model=ResponseModel)
def is_online(request: Request):
    service: UiServer = request.app.state.ui_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

