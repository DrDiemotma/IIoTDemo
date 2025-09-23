import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from UiNode.UiServer import UiServer
from UiNode.routes import router
import Common.Logging.setup

ui_server: UiServer = UiServer()

@asynccontextmanager
async def lifespan(application: FastAPI):
    Common.Logging.setup("UiServer", logging.INFO)
    await ui_server.register()
    yield
    ui_server.shutdown()

app = FastAPI(lifespan=lifespan)

app.state.ui_server = ui_server
app.include_router(router)
