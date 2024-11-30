from typing import List

from . import Command


class SimpleMacroCommand(Command):
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands

    def execute(self):
        for command in self.commands:
            command.execute()
