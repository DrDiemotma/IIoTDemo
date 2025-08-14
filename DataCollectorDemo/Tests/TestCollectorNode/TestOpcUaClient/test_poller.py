import asyncio

import pytest
from asyncua import Node

from CollectorNode.OpcUaClient import Poller, OpcUaConfig, NodeConfig
from Common.Communication import DataMessageModel
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
    waited = 0
    while not test_server.running and waited < 3:
        await asyncio.sleep(1)  # sleep for a second to let the server start

    assert test_server.running
    node: Node = test_server.get_node()
    assert node is not None
    message: list[DataMessageModel] = []
    def pc(x: DataMessageModel, m):
        m.append(x)

    sut: Poller = Poller(node=node, name="TestPoller", polling_rate=50, publish_callback=lambda x: pc(x, message))
    sut.start()

    waited = 0
    while waited < 3 and len(message) == 0:
        await asyncio.sleep(1)

    assert len(message) > 0
    print(message[0])

    

