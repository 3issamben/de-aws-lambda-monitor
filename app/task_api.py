import requests
from .logger_config import logger
from .utils import is_json
import os

api_base_url = os.environ.get(
    "API_BASE_URL",
    "https://ems.digitaledge.net/service4/cmon/TaskController.aspx",
)


def make_request(url, data):
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error occurred: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        logger.error(f"Error occurred: {err}")
        return None

    if is_json(response.text):
        return response.json()

    logger.error("Response was not JSON")
    return None


def task_api(action, parameters):
    api_url = f"{api_base_url}?sp={action}"

    logger.info(f"Calling method {action} with params {parameters}")

    response = make_request(api_url, parameters)

    if response:
        return response
    else:
        logger.info("response was empty")
        return None
