import httpx
import logging

def is_server_online(url: str, timeout: float) -> bool:
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url)
            return response.status_code == 200
    except Exception as e:
        logging.error(f"Server not available: {e}.")
        return False

def is_initialized(url: str, timeout: float) -> bool:
    call = f"{url}/is_initialized"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(call)
            if response.status_code == 200:
                initialized = response.json()
                logging.info(f"Initialization requested, response: {initialized}")
                return initialized
            else:
                logging.error(f"Not able to request initialization status: {response}")
                return False
    except Exception as e:
        logging.error(f"Exception caught while trying to receive initialization status: {e}")
        return False


def get_sensors(url: str, timeout: float) -> dict:
    call = f"{url}/get_sensors"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(call)
            if response.status_code == 200:
                return response.json()

            logging.error(f"Error calling server: {response.status_code}.")
            return {}

    except Exception as e:
        logging.error(f"Server offline or error: {e}")
        return {}

def add_sensor(url: str, payload: dict, timeout: float) -> bool:
    call = f"{url}/add_sensor"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call, json=payload)
            if response.status_code == 200:
                logging.info(f"Added sensor with payload: {payload}")
                return True
            else:
                logging.error(f"Sensor not added: {response}")
                return False

    except Exception as e:
        logging.error(f"Error caught while trying to add a sensor: {e}")
        return False


def delete_sensor(url: str, payload: dict, timeout: float) -> bool:
    call = f"{url}/delete_sensor"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call, json=payload)
            if response.status_code == 200:
                logging.info(f"Successfully deleted sensor {payload['type']} {payload['identifier']}")
                return True
            else:
                logging.error(f"Sensor not deleted: {response}")
                return False

    except Exception as e:
        logging.error(f"Error caught while trying to add a sensor: {e}")
        return False

def initialize(url: str, timeout: float) -> bool:
    call = f"{url}/initialize"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call)
            if response.status_code == 200:
                logging.info("Machine initialization successfully called.")
                return response.json()
            else:
                logging.error(f"Could not call the initialization: {response}")
                return False
    except Exception as e:
        logging.error(f"Error caught while trying to initialize the server: {e}")
        return False

def start_server(url: str, timeout: float) -> None:
    call = f"{url}/start"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call)
            if response.status_code == 200:
                logging.info("Machine started.")
                return
            else:
                logging.error(f"Could not start the machine: {response}")
    except Exception as e:
        logging.error(f"Exception caught while trying to start the machine: {e}")

def stop_server(url: str, timeout: float) -> None:
    call = f"{url}/stop"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call)
            if response.status_code == 200:
                logging.info("Machine stopped")
            else:
                logging.error(f"Could not stop the machine: {response}")
    except Exception as e:
        logging.error(f"Exception caught while trying to stop the machine: {e}")

def is_server_running(url: str, timeout: float) -> bool:
    call = f"{url}/is_running"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(call)
            response_value = response.json()
            if response.status_code == 200:
                logging.info(f"Requested server running status. is running: {response_value}")
                return response_value
            else:
                logging.error(f"Could not determine running status: {response}")
                return False
    except Exception as e:
        logging.error(f"Caught exception while trying to receive running status: {e}")

    return False

def is_job_running(url: str, timeout: float) -> bool:
    call = f"{url}/is_job_running"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(call)
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Requested job running, status: {result}")
                return result
            else:
                logging.error(f"Could not get the job status: {response}")
                return False
    except Exception as e:
        logging.error(f"Caught exception while trying to receive job status: {e}")

    return False

def start_job(url: str, timeout: float) -> None:
    call = f"{url}/start_job"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call)
            if response.status_code == 200:
                logging.info("Started job running.")
            else:
                logging.error(f"Could not start the job: {response}")
    except Exception as e:
        logging.error(f"Caught exception while trying to start the job: {e}")

def stop_job(url: str, timeout: float) -> None:
    call = f"{url}/stop_job"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(call)
            if response.status_code == 200:
                logging.info("Stopped the job.")
            else:
                logging.error(f"Could not stop the job: {response}")
    except Exception as e:
        logging.error(f"Caught exception while trying to stop the job: {e}")
