from fastapi import APIRouter, Request

from UiNode.UiServer import UiServer
from Common.Communication import ResponseFactory, ResponseModel, CommandModel, ConfigurationModel

router: APIRouter = APIRouter()

@router.get("/", response_model=ResponseModel)
def root_call():
    return ResponseFactory.ok(values="UiServer")

@router.get("/is_online", response_model=ResponseModel)
def is_online(request: Request):
    service: UiServer = request.app.state.ui_server
    response: bool = service.is_online
    return ResponseFactory.ok(values=response)

@router.post("/save_config", response_model=ResponseModel)
def save_config(configuration: CommandModel, request: Request):
    service: UiServer = request.app.state.ui_server
    if not isinstance(configuration.parameters, ConfigurationModel):
        return ResponseFactory.nok(f"Expected type CommandModel, got {type(configuration.parameters)} instead.")

    config: ConfigurationModel = configuration.parameters
    service.write_config(config)
    return ResponseFactory.ok()
