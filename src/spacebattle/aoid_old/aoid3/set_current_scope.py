from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, init_command, scope):
        self.init_command = init_command
        self.scope = scope

    def execute(self):
        self.init_command.current_scopes.value = self.scope
