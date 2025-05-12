from src.spacebattle.commands.command import Command


class ClearCurrentScopeCommand(Command):
    def execute(self):
        from src.spacebattle.commands.init import InitCommand

        if hasattr(InitCommand.current_scope, "value"):
            del InitCommand.current_scope.value
