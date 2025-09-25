import abc
import asyncio
import logging
from abc import abstractmethod

from httpx import Response

from Common.Communication import CommandModel, MessageCategory
from Common.Communication import ResponseModel
from Common.Model import ServerOutline
import httpx


class ServerBase(abc.ABC):
    """BaseNode class for all servers."""
    def __init__(self, name: str, port: int):
        logging.info(f"Initializing server \"{name}\" on port {port}.")
        self.__name: str = name
        self.__server_active: bool = False
        self.__shutdown_finished: bool = False
        self.__port = port

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logging.info("Shutting down gracefully.")
        await self.shutting_down()
        logging.info("Shutdown complete. Goodbye.")

    @property
    def name(self) -> str:
        """Get the name of the server. This is used for the display of the """
        return self.__name

    @property
    def port(self) -> int:
        """Port at which the server is reachable."""
        return self.__port

    @property
    def _active(self):
        """Whether the server is active."""
        return self.__server_active

    @_active.setter
    def _active(self, value: bool):
        self.__server_active = value

    @property
    @abstractmethod
    def is_online(self):
        """Whether the server is active. Difference to :attr ServerBase._active: is that
         this checks that all conditions are met to be online, i.e., that all resources are available."""
        pass

    async def shutting_down(self):
        if self.__shutdown_finished:
            logging.warning(f"Server \"{self.name}\" already shut down.")
            return
        await self.shutdown()
        self.__shutdown_finished = True
        logging.info(f"Server \"{self.name}\" shut down. Goodbye!")

    @abstractmethod
    async def shutdown(self):
        """Shut down the server."""
        pass

    @abstractmethod
    def on_new_data(self, dataset):
        pass

    @abstractmethod
    def get_outline(self) -> ServerOutline:
        pass

    async def register(self, control_server_port: int = 8000,
                       control_server_command: str = "register",
                       retries: int = 5, wait_for_seconds: float = 1):
        """Register the server to the control server."""
        logging.info(f"Starting registering server \"{self.name}\" on port {control_server_port}" 
                     f"(command: {control_server_command}, {retries=}, wait time={wait_for_seconds}).")
        server_outline = self.get_outline()
        server_url = f"http://localhost:{control_server_port}/{control_server_command}"
        outline = server_outline.model_dump()

        async with httpx.AsyncClient() as client:
            tries = 0
            success = False
            while not success and tries < retries:
                logging.info(f"Register \"{self.name}\" to server {tries+1}/{retries}...")
                http_response: Response = await client.post(
                    server_url,
                    json=outline
                )
                try:
                    response: ResponseModel = ResponseModel(**(http_response.json()))
                except Exception as e:
                    logging.warning(f"\"{self.name}\": converting not successful: {e}")
                    tries += 1
                    await asyncio.sleep(wait_for_seconds)
                    continue
                if response.message_result == MessageCategory.ok:
                    logging.info(f"\"{self.name}\": successfully registered")
                    success = True
                else:
                    logging.error(f"\"{self.name}\": registration failed: {response.return_message}")
                    await asyncio.sleep(wait_for_seconds)
                    tries += 1

            if not success:
                logging.error(f"Failed to register service \"{self.name}\".")


