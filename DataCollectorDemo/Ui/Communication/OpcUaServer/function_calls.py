import httpx
import logging

def is_server_online(url: str, timeout: float):
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url)
            return response.status_code == 200
    except Exception as e:
        logging.error(f"Server not available: {e}.")
        return False


def get_sensors(url: str, timeout: float):
    call = f"{url}/get_sensors"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(call)
            if response.status_code == 200:
                return response.json()

            logging.error(f"Error calling server: {response.status_code}.")
            return []

    except Exception as e:
        logging.error(f"Server offline or error: {e}")
        return []

def add_sensor(url: str, payload: dict, timeout: float):
    call = f"{url}/add_sensor"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call, json=payload)
            if response.status_code == 200:
                logging.info(f"Added sensor with payload: {payload}")
                return True
            else:
                logging.error(f"Sensor not added: {response}")

    except Exception as e:
        logging.error(f"Error caught while trying to add a sensor: {e}")
        return False


