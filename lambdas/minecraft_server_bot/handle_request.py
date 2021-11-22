import argparse
import logging
from typing import Callable, Optional

import boto3
from command import Command
from config import INSTANCE_ID, SLACK_CHANNEL
from instance_state import InstanceState
from request import Request
from responses import Responses
from slack import respond

logger = logging.getLogger()
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument(
    "command",
    choices=Command,
    type=Command,
)
parser.add_argument("-q", "--quiet", action="store_true")


def handle_request(params: dict) -> dict:
    request = _parse_request(params)

    if not request:
        return respond(Responses.USAGE.value)

    logger.info(request)

    if request.channel != SLACK_CHANNEL:
        return respond(Responses.WRONG_CHANNEL.value)

    if request.command == Command.PRAY:
        return respond(Responses.PRAY.value, request.quiet)

    return _handle_state_request(request)


def _parse_request(params: dict) -> Optional[Request]:
    user = params["user_name"][0]
    channel = params["channel_name"][0]
    text = params.get("text", [""])[0].split(" ")

    command = None
    quiet = False

    try:
        args = parser.parse_args(text)
        command = args.command
        quiet = args.quiet
    except Exception as e:
        logger.error(e)

    return (
        Request(user=user, channel=channel, command=command, quiet=quiet)
        if command
        else None
    )


def _handle_state_request(request: Request) -> dict:
    ec2 = boto3.resource("ec2")
    instance = ec2.Instance(INSTANCE_ID)
    instance_state = InstanceState(instance.state["Name"].lower())

    if request.command == Command.STATUS:
        return respond(Responses.instance_state(instance_state), request.quiet)

    if (
        request.command == Command.START
        and instance_state == InstanceState.STOPPED
    ):
        return _attempt_state_change(instance.start, request)
    elif (
        request.command == Command.STOP
        and instance_state == InstanceState.RUNNING
    ):
        return _attempt_state_change(instance.stop, request)
    else:
        return respond(
            Responses.invalid_state_change(request, instance_state),
            request.quiet,
        )


def _attempt_state_change(action: Callable, request: Request) -> dict:
    try:
        action()
        return respond(
            Responses.state_change(request.user, request.command), request.quiet
        )
    except Exception as e:
        logger.error(e)
        return respond(
            Responses.error_for_command(request.command), request.quiet
        )
