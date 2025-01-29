from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, scope):
        self._scope = scope

    def execute(self):
        from src.spacebattle.commands.init import InitCommand

        InitCommand.current_scope.value = self._scope
