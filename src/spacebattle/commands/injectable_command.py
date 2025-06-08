from src.spacebattle.commands.command import Command
from src.spacebattle.commands.injectable import Injectable


class InjectableCommand(Command, Injectable):
    def __init__(self):
        self.__command = None

    def execute(self):
        self.__command.execute()

    def inject(self, command: Command):
        self.__command = command
