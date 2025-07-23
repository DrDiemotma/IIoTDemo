from fastapi import FastAPI
from ControlNode.routes import router
from ControlNode.Server import ControlServer


app: FastAPI = FastAPI()
control_server: ControlServer = ControlServer()
app.state.control_server = control_server
app.include_router(router)


if __name__ == "__main__":
    import multiprocessing
    import uvicorn


    def start_service(port: int = 8000):
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
