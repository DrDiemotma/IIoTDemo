from CollectorNode.OpcUaClient import OpcUaManagingServer, OpcUaConfig
from Common.Communication import Command, ResponseModel, MessageCategory


def test_execute_command_add_config():
    sut = OpcUaManagingServer()
    config = OpcUaConfig(server_id="TestServer", ip="127.0.0.1", uri="TestServerUri")
    command_add: Command = Command(sender="Test", target=sut.server_namespace, command="add_config",
                                   parameters=[config])
    response: ResponseModel = sut.execute_command(command_add)
    if response.return_message is not None:
        print(response.return_message)
    assert response.message_result == MessageCategory.ok

def test_execute_command_read_configs():
    sut = OpcUaManagingServer()
    config = OpcUaConfig(server_id="TestServer", ip="127.0.0.1", uri="TestServerUri")
    command_add: Command = Command(sender="Test", target=sut.server_namespace, command="add_config",
                                   parameters=[config])
    _ = sut.execute_command(command_add)
    command_read: Command = Command(sender="Test", target=sut.server_namespace, command="get_configs")
    response: ResponseModel = sut.execute_command(command_read)
    if response.return_message is not None:
        print(response.return_message)
    assert response.message_result == MessageCategory.ok
    response_configs: list[OpcUaConfig] | None = response.return_value
    assert len(response_configs) == 1
    for response_config in response_configs:
        assert isinstance(response_config, OpcUaConfig)
    ...

def test_on_new_data():
    ...
