import asyncio

import httpx
from httpx import HTTPStatusError

from Common.Communication import ResponseModel


async def get_services_async(control_server_port: int = 8000, retries: int = 5) -> list[str]:
    """
    Get the microservices which are currently running.
    :param control_server_port: Port for the control server.
    :param retries: How many retries are performed.
    :return: List of service names or representations of errors.
    """
    server_url: str = f"http://localhost:{control_server_port}/get_services"
    async with httpx.AsyncClient() as client:
        tries = 0
        success = False

        last_error = None

        while not success and tries < retries:
            try:
                http_response = await client.get(server_url)
                response: ResponseModel = ResponseModel(**(http_response.json()))
            except (HTTPStatusError, httpx.ConnectError) as http_error:
                await asyncio.sleep(1)
                last_error = http_error
                tries += 1
                continue
            except Exception as e:
                return [repr(e)]

            success = True

        return response.return_value if success else [last_error]
