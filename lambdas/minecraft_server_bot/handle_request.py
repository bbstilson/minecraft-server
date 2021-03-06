import argparse
import logging
from time import time

from typing import Callable, List, Optional

import boto3
from command import Command
from config import INSTANCE_ID, SLACK_CHANNEL
from instance_state import InstanceState
from request import Request
from responses import Responses
from slack import respond

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise Exception(f"Could not parse arguments: {message}")


parser = ArgumentParser()
parser.add_argument(
    "command",
    choices=Command,
    type=Command,
)
parser.add_argument("-q", "--quiet", action="store_true")


def timed(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


@timed
def handle_request(params: dict) -> dict:
    request = _parse_request(params)

    if not request:
        return respond(Responses.USAGE.value, True)

    logger.info(request)

    if request.channel != SLACK_CHANNEL:
        return respond(Responses.WRONG_CHANNEL.value, request.quiet)

    if request.command == Command.PRAY:
        return respond(Responses.PRAY.value, request.quiet)

    return _handle_state_request(request)


@timed
def _parse_request(params: dict) -> Optional[Request]:
    text: List[str] = [
        arg for arg in params.get("text", [""])[0].split(" ") if arg
    ]

    try:
        args = parser.parse_args(text)
        return Request(
            user=params["user_name"][0],
            channel=params["channel_name"][0],
            command=args.command,
            quiet=args.quiet,
        )
    except Exception as e:
        logger.error(e)
        return None


@timed
def get_instance():
    ec2 = boto3.resource("ec2")
    return ec2.Instance(INSTANCE_ID)


@timed
def get_instance_state(instance):
    return InstanceState(instance.state["Name"].lower())


@timed
def _handle_state_request(request: Request) -> dict:
    instance = get_instance()
    instance_state = get_instance_state(instance)

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


@timed
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
