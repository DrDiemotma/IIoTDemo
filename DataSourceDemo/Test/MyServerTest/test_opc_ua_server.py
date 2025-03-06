import asyncio

from MyServer import opc_ua_server
import unittest


class TestOpcUaTestServer(unittest.TestCase):
    def setUp(self):
        self.sut = opc_ua_server.OpcUaTestServer()

    def test_start(self):
        asyncio.run(self.sut.start())
        asyncio.run(asyncio.sleep(opc_ua_server.FREQ * 10))
        asyncio.run(self.sut.stop())

if __name__ == '__main__':
    unittest.main()
