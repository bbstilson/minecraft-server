import json
import logging
import os

import urllib3

INSTANCE_ID = "i-0f4053b9802682c04"
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
http = urllib3.PoolManager()


def lambda_handler(event, context):
    detail = event["detail"]

    logger.info(detail)

    instance_id = detail["instance-id"]
    state = detail["state"]

    if instance_id == INSTANCE_ID:
        http.request(
            "POST",
            SLACK_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "response_type": "in_channel",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"The server is {state}.",
                            },
                        }
                    ],
                }
            ).encode("utf8"),
        )
        logger.info("Sent status update.")
    else:
        logger.error("Wrong instance id.")
