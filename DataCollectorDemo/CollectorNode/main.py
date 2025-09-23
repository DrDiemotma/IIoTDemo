import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from CollectorNode.routes import router
from CollectorNode.OpcUaClient import OpcUaManagingServer
import Common.Logging.setup

opc_ua_managing_server: OpcUaManagingServer = OpcUaManagingServer()

@asynccontextmanager
async def lifespan(application: FastAPI):
    Common.Logging.setup("CollectorNode", logging.INFO)
    managing_server: OpcUaManagingServer = application.state.opc_ua_managing_server

    await managing_server.register()
    yield

app = FastAPI(lifespan=lifespan)

app.state.opc_ua_managing_server = opc_ua_managing_server
app.include_router(router)


if __name__ == '__main__':
    import multiprocessing
    import uvicorn


    def start_service(port: int = 8001):
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
