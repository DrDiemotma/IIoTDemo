from dataclasses import dataclass

PROTOCOL: str = "opc.tcp"

@dataclass
class OpcUaConfig:
    ip: str
    port: int
    server_id: str
    uri: str

    def get_url(self) -> str:
        result: str = f"{PROTOCOL}://{self.ip}:{self.port}/{self.server_id}"
        return result
