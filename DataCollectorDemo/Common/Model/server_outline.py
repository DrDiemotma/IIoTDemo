from pydantic import BaseModel


class ServerOutline(BaseModel):
    """
    Register information for a server.
    """
    port: int
    """Port of the server to be used."""

    name: str
    """Name of the server."""

    sensor_data_receiver: bool = False
    """Whether the server is meant to be called when new sensor data is received. 
    This is not to be confused with configuration."""

    sensor_data_sender: bool = False
    """Whether te server sends measurement data."""

    class Config:
        frozen = True
