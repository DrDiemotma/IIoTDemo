from fastapi import FastAPI
from CollectorNode.routes import router
from CollectorNode.OpcUaClient import OpcUaManagingServer


app = FastAPI()
opc_ua_managing_server: OpcUaManagingServer = OpcUaManagingServer()
app.state.opc_ua_managing_server = opc_ua_managing_server
app.include_router(router)

