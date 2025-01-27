from src.spacebattle.commands.command import Command


class ClearCurrentScopeCommand(Command):
    def __init__(self, init_command):
        self.init_command = init_command

    def execute(self):
        self.init_command.scope = {}
