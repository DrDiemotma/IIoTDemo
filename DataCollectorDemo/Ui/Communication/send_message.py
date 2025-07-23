from Ui.Communication import (
    Target
)
from Common.Communication import ActivitySelection, Command, ResponseModel
import requests
from typing import Any


def send_message(target_url: str, command: Command):
    """
    Send a message to the server.
    :param target_url: URL to the target.
    :param command: Command to execute.
    :return: Response as a dictionary.
    """
    payload = command.__dict__
    try:
        response = requests.post(target_url, json=payload)
        if response is None:
            return None
        else:
            return response.json()
    except Exception as e:
        # todo find out which errors occur, for example, server not reachable 
        print(e)
        raise

