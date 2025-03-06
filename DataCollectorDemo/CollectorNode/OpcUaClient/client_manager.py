from threading import Lock
from CollectorNode.OpcUaClient import OpcUaClient
from CollectorNode.OpcUaClient import OpcUaConfig

class SingletonMeta(type):
    """
    Thread-safe version of a singleton pattern. Use for configuration managers.
    """
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class ClientManager(metaclass=SingletonMeta):
    """
    Simple client manager singleton.
    """
    def __init__(self):
        self._clients: dict[str, OpcUaClient] = {}

    def get_client(self, ip_address: str, port: int) -> OpcUaClient | None:
        name = self._get_name(ip_address, port)
        if name not in self._clients:
            return None

        return self._clients[name]


    def set_client(self, config: OpcUaConfig) -> bool:
        name: str = self._get_name(config.ip, config.port)
        if name in self._clients:
            return False

        client: OpcUaClient = OpcUaClient()
        client.config = config
        self._clients[name] = client
        return True

    @staticmethod
    def _get_name(ip_address: str, port: int):
        return f"{ip_address}:{port}"
