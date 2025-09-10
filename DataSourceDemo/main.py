from MyServer import opc_ua_server
from fastapi import FastAPI
from MyServer.Api import router

app = FastAPI(title="OPC UA Server Demo")
server = opc_ua_server.OpcUaTestServer()
app.state.server = server
app.include_router(router)


if __name__ == '__main__':
    import multiprocessing
    import uvicorn
    def start_service(port: int = 8765):
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)

    process: multiprocessing.Process = multiprocessing.Process(target=start_service)
    process.start()
