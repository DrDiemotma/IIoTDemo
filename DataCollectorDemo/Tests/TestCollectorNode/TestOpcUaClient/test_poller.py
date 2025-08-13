import pytest
from asyncua import Node
from uvicorn.loops.asyncio import asyncio_setup

from CollectorNode.OpcUaClient import Poller, OpcUaConfig, NodeConfig
from Tests.TestServer import OpcUaTestServer


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


@pytest.mark.asyncio
async def test_start_stop():
    test_server = OpcUaTestServer(test_config.get_url())
    await test_server.start()
    node: Node = test_server.get_node()
    assert node is not None
    

