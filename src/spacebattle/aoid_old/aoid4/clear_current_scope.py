from src.spacebattle.commands.command import Command


class ClearCurrentScopeCommand(Command):
    def execute(self):
        from src.spacebattle.aoid4.init import InitCommand

        InitCommand.current_scopes.value = None
