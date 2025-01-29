from src.spacebattle.commands.command import Command


class ClearCurrentScopeCommand(Command):
    def execute(self):
        from src.spacebattle.commands.init import InitCommand

        InitCommand.current_scope.value = None
