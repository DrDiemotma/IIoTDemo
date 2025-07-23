from BaseNode.Server import ServerBase
from ControlNode.Server import ControlServer
from Common.Communication import Command, ActivitySelection, MessageCategory, ResponseModel, ResponseFactory
from Common.Model import ServerOutline


class TestServer(ServerBase):
    """
    Mockup server for testing purposes.
    """

    def get_outline(self) -> ServerOutline:
        return ServerOutline(
            name=self.name,
            port=self.port
        )

    def shutdown(self):
        pass

    def on_new_data(self, dataset):
        pass

    _execute_command_called: int = 0
    _last_command: str | None = None

    def execute_command(self, command: Command) -> ResponseModel:
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
        super().__init__(name, 8999)


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
    sut.register_server(test_server.get_outline())

def test_execute_command_to_control_server():
    sut: ControlServer = ControlServer()
    cmd: Command = Command(sender="Test", type_=ActivitySelection.get_info, command="get_servers", target=sut.server_namespace)
    result: ResponseModel = sut.execute_command(cmd)
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


