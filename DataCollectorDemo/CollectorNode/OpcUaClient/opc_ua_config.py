from dataclasses import dataclass

PROTOCOL: str = "opc.tcp"

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

    def get_url(self) -> str:
        result: str = f"{PROTOCOL}://{self.ip}:{self.port}/{self.server_id}"
        return result
