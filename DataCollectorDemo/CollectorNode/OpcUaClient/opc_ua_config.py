import os.path
import json
from dataclasses import dataclass, field

PROTOCOL: str = "opc.tcp"

@dataclass(frozen=True)
class NodeConfig:
    """Configuration entry for a field."""
    namespace: str
    """Namespace in the OPC UA configuration."""
    object_name: str
    """Name of the object to subscribe to."""
    value_name: str
    """Name of the object value to receive."""

@dataclass(frozen=True)
class OpcUaConfig:
    """Configuration for OPC UA connections."""
    ip: str
    """IP address of the server."""
    server_id: str
    """ID of the server to connect to."""
    uri: str
    """Server URI."""
    port: int = 4840
    """Port to address the server."""
    subscriptions: list[NodeConfig] = field(default_factory=list)

    def get_url(self) -> str:
        """
        Get the URL from the properties of the configuration.
        :return: The URL to connect to.
        """
        result: str = f"{PROTOCOL}://{self.ip}:{self.port}/{self.server_id}"
        return result


def save_config(config: OpcUaConfig, file_path: str):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except:
            raise
    try:
        with open(file_path, "w") as f:
            json.dump(config, f, cls=NodeConfigJsonEncoder, indent=4)
    except:
        raise




def load_config(file_path: str) -> OpcUaConfig:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    try:
        with open(file_path, "r") as f:
            data = json.load(f, cls=NodeConfigJsonDecoder)
    except OSError as ose:
        print(f"Could not open file: {ose}")
        raise ose

    return data

class NodeConfigJsonEncoder(json.JSONEncoder):
    """Custom JSON config encoder for OPC UA and node configs."""
    def default(self, o: object):
        if isinstance(o, OpcUaConfig):
            return self._opc_ua_config_encoder(o)
        if isinstance(o, NodeConfig):
            return self._node_config_encoder(o)

        return super().default(o)

    def _opc_ua_config_encoder(self, opc_ua_config: OpcUaConfig):
        return opc_ua_config.__dict__

    def _node_config_encoder(self, node_config: NodeConfig):
        return node_config.__dict__


class NodeConfigJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct: dict):
        # NodeConfig
        if "namespace" in dct and "object_name" in dct and "value_name" in dct:
            return NodeConfig(**dct)
        if "ip" in dct and "server_id" in dct and "uri" in dct and "port" in dct and "subscriptions" in dct:
            try:
                return OpcUaConfig(**dct)
            except:
                raise

        return dct
