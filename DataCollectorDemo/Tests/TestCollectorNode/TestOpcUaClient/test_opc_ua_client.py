import asyncio
import json
import os.path
import pytest

from Tests.TestServer import OpcUaTestServer

from CollectorNode.OpcUaClient import OpcUaClient, OpcUaClientFactory, OpcUaConfig, NodeConfig

test_config: OpcUaConfig = OpcUaConfig(
    ip="127.0.0.1",
    server_id="TestServer",
    uri="test_server",
    port=4840,
    subscriptions=[
        NodeConfig(namespace="http://test.org",
                   object_name="TestObject",
                   value_name="TestVariable")
    ]
)

def test_opc_ua_config_get_url():
    url: str =test_config.get_url()
    assert len(url) > 0

def test_opc_ua_client_factory_new_from_config():
    client: OpcUaClient | None = OpcUaClientFactory.new(test_config)
    assert client is not None

def test_opc_ua_client_factory_new_from_file():
    file_name = "test.json"

    def clean_up():
        if os.path.isfile(file_name):
            try:
                os.remove(file_name)
            except OSError as ose_delete:
                print(f"Could not delete file: {ose_delete}")

    clean_up()

    with open(file_name, "w") as f:
        try:
            json.dump(test_config.__dict__, f)
        except OSError as ose_write:
            print(f"Could not write config: {ose_write}.")

    client: OpcUaClient | None = OpcUaClientFactory.new(file_name)
    clean_up()

    assert client is not None

@pytest.mark.asyncio
async def test_connect():
    class DataReceiver:
        def __init__(self):
            self.data_received = False

        def data_callback(self, data):
            print(data)
            self.data_received = True

    data_receiver = DataReceiver()

    server = OpcUaTestServer(test_config.get_url())
    await server.start()
    client: OpcUaClient = OpcUaClientFactory.new(test_config)
    await client.connect()
    client.handler.subscribe(data_receiver.data_callback)
    for i in range(0, 10):
        await server.write(100 + i)
        await asyncio.sleep(1)
        if data_receiver.data_received:
            break

    assert data_receiver.data_received





