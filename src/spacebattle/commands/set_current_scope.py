from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, scope):
        self.scope = scope

    def execute(self):
        from src.spacebattle.commands.init import InitCommand

        InitCommand.scope = self.scope
