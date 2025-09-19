from MyServer import opc_ua_server
from fastapi import FastAPI
from MyServer.Api import router
from MyServer.Lifetime import MachineModel
import logging
from logging.handlers import RotatingFileHandler

app = FastAPI(title="OPC UA Server Demo")
machine_model: MachineModel = MachineModel()
server = opc_ua_server.OpcUaTestServer(machine=machine_model)
app.state.server = server
app.include_router(router)


if __name__ == '__main__':

    handler = RotatingFileHandler(
        "DataSourceDemo.log",
        maxBytes=10_485_760, # 10 MB,
        backupCount=10
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[handler]
    )

    logging.info("Start the OPC UA Server.")
    import multiprocessing
    import uvicorn
    def start_service(port: int = 8765):
        logging.info(f"Starting FastAPI service on port {port}.")
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
