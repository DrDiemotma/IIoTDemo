import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import Common.Logging.setup
from ControlNode.routes import router
from ControlNode.Server import ControlServer

@asynccontextmanager
async def lifespan(application: FastAPI):
    Common.Logging.setup("ControlNode", logging.INFO)
    logging.info("Starting the ControlServer.")
    control_server: ControlServer = ControlServer()
    application.state.control_server = control_server
    yield
    control_server.shutdown()
    logging.info("Shut down gracefully.")

app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import multiprocessing
    import uvicorn


    def start_service(port: int = 8000):
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
