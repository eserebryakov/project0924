from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, scope):
        self.scope = scope

    def execute(self):
        from src.spacebattle.aoid4.init import InitCommand

        InitCommand.current_scopes.value = self.scope
