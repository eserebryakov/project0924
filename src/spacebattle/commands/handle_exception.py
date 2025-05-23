from src.spacebattle.commands.command import Command


class HandleExceptionCommand(Command):
    def __init__(self, command: Command, exception: Exception):
        self.command = command
        self.exception = exception

    def execute(self):
        print(type(self.exception))
        print(type(self.command))
