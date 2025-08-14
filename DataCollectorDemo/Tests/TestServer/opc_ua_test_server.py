import asyncio
import asyncua
from asyncua import ua

class OpcUaTestServer:
    """
    Test server class for OPC UA. Used for unit tests.
    """
    def __init__(self, endpoint: str,
                 server_name: str = "TestServer",
                 test_namespace: str = "http://test.org",
                 object_name: str = "TestObject",
                 variable_name: str = "TestVariable"):
        """
        ctor.
        :param endpoint:
        :param server_name:
        :param test_namespace:
        :param object_name:
        :param variable_name:
        """
        self._endpoint: str = endpoint
        self._server: asyncua.Server = asyncua.Server()
        self._idx: int | None = None
        self._var: asyncua.Node | None = None
        self._server_task: asyncio.Task[None] | None = None
        self._server_name: str = server_name
        self._test_namespace: str = test_namespace
        self._object_name: str = object_name
        self._variable_name = variable_name
        self._running: bool = False


    async def start(self, start_value: int = 42):
        self._server.set_endpoint(self._endpoint)
        self._server.set_server_name(self._server_name)
        try:
            await asyncio.wait_for(self._server.init(), timeout=15)
        except:
            print("Timeout while initializing the OPC UA server.")
            raise
        self._idx = await self._server.register_namespace(self._test_namespace)
        obj: asyncua.Node = await self._server.nodes.objects.add_object(self._idx, self._object_name)
        self._var = await obj.add_variable(self._idx, self._variable_name, start_value, varianttype=ua.VariantType.Int32)
        await self._var.set_writable()
        access_level = ua.AccessLevel.CurrentRead | ua.AccessLevel.CurrentWrite
        variant = ua.Variant(access_level, ua.VariantType.Byte)
        data_value = ua.DataValue(variant)
        await self._var.write_attribute(ua.AttributeIds.AccessLevel, data_value)
        await self._var.write_attribute(ua.AttributeIds.UserAccessLevel, data_value)
        self._server_task = asyncio.create_task(self._server.start())
        self._running = True

    async def stop(self):
        if self._server:
            await self._server.stop()
        if self._server_task:
            self._server_task.cancel()
        self._running = False

    @property
    def running(self):
        return self._running

    def get_node(self):
        return self._var

    async def write(self, value: int):
        assert self._var is not None
        await self._var.write_value(value, varianttype=ua.VariantType.Int32)
