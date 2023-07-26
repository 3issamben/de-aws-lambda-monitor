from .logger_config import logger
from urllib.parse import urlsplit
import socket
import json
from datetime import datetime


def _get_base_url(url):
    # get task base url
    if url is not None:
        # TODO  check if url is valid format (use reg exp)
        base_url = "{0.netloc}".format(urlsplit(url))
        logger.info(f"Resolving {base_url}")
    else:
        logger.error(f"provided url is not valid {url}")
        raise ValueError
    return base_url


def dns_resolution(url):
    dns_resolution = False
    try:
        base_url = _get_base_url(url)
        socket.gethostbyname_ex(base_url)
        ip_list = [
            i[-1][0] for i in socket.getaddrinfo(base_url, None)
        ]

        if len(ip_list) > 0:
            logger.info(
                f"dns resolution of url {url} returned {ip_list}"
            )
            dns_resolution = True

    except Exception as e:
        logger.error(f"DNS resolution failed with {str(e)}")

    return dns_resolution


def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return False


def calculate_execution_time(logs):
    lines = logs.split("\n")
    lines = [line for line in lines if line]

    if not lines:
        return None

    timestamp_format = "%Y-%m-%d %H:%M:%S,%f"

    start_time = datetime.strptime(
        lines[0].split(" - ")[0], timestamp_format
    )
    end_time = datetime.strptime(
        lines[-1].split(" - ")[0], timestamp_format
    )

    execution_time = end_time - start_time

    return execution_time.total_seconds()
