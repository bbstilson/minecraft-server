from dataclasses import dataclass

from command import Command


@dataclass
class Request:
    user: str
    channel: str
    command: Command
    quiet: bool
