from MyServer import opc_ua_server
from fastapi import FastAPI

app = FastAPI()
server = opc_ua_server.OpcUaTestServer()
app.state.server = server


if __name__ == '__main__':
    import multiprocessing
    import uvicorn
    def start_service(port: int = 4840):
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
