from fastapi import FastAPI
from contextlib import asynccontextmanager
from UiNode.UiServer import UiServer
from UiNode.routes import router

ui_server: UiServer = UiServer()

@asynccontextmanager
async def lifespan(application: FastAPI):
    await ui_server.register()
    yield

app = FastAPI(lifespan=lifespan)

app.state.ui_server = ui_server
app.include_router(router)
