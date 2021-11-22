from enum import Enum

from command import Command
from config import SLACK_CHANNEL
from instance_state import InstanceState
from request import Request


class Responses(Enum):
    INVALID_REQUEST_TOKEN = "Invalid Request Token"
    PRAY = "⛧ A̶L̷L̵ ̶H̷A̶I̶L̴ ̴T̸H̶E̸ ̵C̷U̴B̷E̸ ⛧"
    WRONG_CHANNEL = f"Please execute this command in #{SLACK_CHANNEL} so that I can yell at everyone :yelling:"
    USAGE = "\n".join(
        [
            "/msb `<command>`",
            "",
            "Available Commands:",
            "",
            "`start` - Start the server.",
            "`stop` - Stop the server.",
            "`status` - Get the server status.",
            "`pray` - Pray to the Cube.",
        ]
    )

    @staticmethod
    def instance_state(instance_state: InstanceState) -> str:
        return f"The server is {instance_state.value}."

    @staticmethod
    def state_change(user: str, command: Command) -> str:
        return f"@here {user} is going to {command.value} the server."

    @staticmethod
    def invalid_state_change(
        request: Request, instance_state: InstanceState
    ) -> str:
        return " ".join(
            [
                f"{request.user} wants to {request.command.value} the server",
                f"but it is {instance_state.value}.",
                "THIS ANGERS THE CUBE.",
            ]
        )

    @staticmethod
    def error_for_command(command: Command) -> str:
        return " ".join(
            [
                f"I tried to {command.value} the server but I hit an error.",
                "Ask Brandon to figure it out.",
            ]
        )
