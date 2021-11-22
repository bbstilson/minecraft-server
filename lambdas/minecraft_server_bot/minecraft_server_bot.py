import logging
from urllib.parse import parse_qs

from config import VERIFICATION_TOKEN
from handle_request import handle_request
from responses import Responses
from slack import respond

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    params = parse_qs(event["body"])
    token = params["token"][0]

    if token != VERIFICATION_TOKEN:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Responses.INVALID_REQUEST_TOKEN.value)

    return handle_request(params)
