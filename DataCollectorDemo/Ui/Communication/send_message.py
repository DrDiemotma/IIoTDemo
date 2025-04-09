from Ui.Communication import (
    Target
)
from Common.Communication import ActivitySelection
import requests
from typing import Any


def send_message(sender: str, target: Target, command: str, *parameters: Any,
                 activity: ActivitySelection = ActivitySelection.action):
    """
    Send a message to the server.
    :param sender: Entity which requests the action.
    :param target: Target entity. Which is to be configured.
    :param command: Command to execute.
    :param parameters: parameters for the command
    :param activity: Activity context.
    :return: Response as a dictionary.
    """
    payload = {
        "sender": sender,
        "type_": activity,
        "command": command,
        "params": list(parameters)
    }
    try:
        response = requests.post(target.url, json=payload)
        if response is None:
            return None
        else:
            return response.json()
    except Exception as e:
        # todo find out which errors occur, for example, server not reachable 
        print(e)
        raise

