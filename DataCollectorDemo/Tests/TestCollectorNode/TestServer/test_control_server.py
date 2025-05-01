import pytest

from CollectorNode.Server import ControlServer, ServerBase
from Common.Communication import Command, ActivitySelection, MessageCategory, Response, ResponseFactory


class TestServer(ServerBase):
    """
    Mockup server for testing purposes.
    """

    def shutdown(self):
        pass

    def on_new_data(self, dataset):
        pass

    _execute_command_called: int = 0
    _last_command: str | None = None

    def execute_command(self, command: Command) -> Response:
        self._execute_command_called += 1
        self._last_command = command.command
        return ResponseFactory.ok()

    @property
    def server_namespace(self):
        return "TEST_SERVER"

    @property
    def is_online(self):
        return self._active

    @property
    def execute_command_called(self) -> int:
        """
        How many times execute_command was called.
        """
        return self._execute_command_called

    def __init__(self, name: str = "Test"):
        super().__init__(name)


def test_activate():
    sut: ControlServer = ControlServer()
    assert sut.is_online == False
    sut.activate()
    assert sut.is_online == True
    sut.deactivate()
    assert sut.is_online == False

def test_register_server():
    sut: ControlServer = ControlServer()
    test_server: TestServer = TestServer()
    test_server2 : TestServer = TestServer()
    assert sut.is_online == False
    assert test_server.is_online == False

    sut.register_server(test_server)
    names: tuple[str, ...] = sut.get_server_names()
    assert "Test" in names
    sut.activate()
    assert test_server.is_online == True
    sut.register_server(test_server2)
    assert test_server2.is_online == True
    sut.deactivate()
    assert test_server.is_online == False
    assert test_server2.is_online == False

def test_execute_command_to_control_server():
    sut: ControlServer = ControlServer()
    cmd: Command = Command(sender="Test", type_=ActivitySelection.get_info, command="get_servers", target=sut.server_namespace)
    result: Response = sut.execute_command(cmd)
    assert result.message_result == MessageCategory.ok
    bad_cmd: Command = Command(sender="Test", type_=ActivitySelection.get_info, command="foo", target=sut.server_namespace)
    result = sut.execute_command(bad_cmd)
    assert result.message_result == MessageCategory.nok
    
def test_execute_command_to_other_server():
    sut: ControlServer = ControlServer()
    test_server: TestServer = TestServer()
    previously_called = test_server.execute_command_called
    sut.register_server(test_server)
    test_command = "test"
    cmd: Command = Command(sender="Test", command=test_command, target=test_server.server_namespace)
    result = sut.execute_command(cmd)
    assert result.message_result == MessageCategory.ok
    assert test_server.execute_command_called == previously_called + 1


