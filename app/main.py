from task_manager import main
import os
from logger_config import logger
import json


# Settings


def lambda_handler(event=None, context=None):
    logger.info("started lambda function")
    try:
        puller_id = event.get("puller_id") or os.environ.get(
            "PULLER_ID", "11"
        )

        result = main(puller_id)

        return {
            "statusCode": 200,
            "body": json.dumps({"result": result}),
        }

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An error occurred"}),
        }
