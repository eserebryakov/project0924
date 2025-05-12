from src.spacebattle.commands.command import Command


class UpdateIocResolveDependencyStrategyCommand(Command):
    def __init__(self, updater):
        self._update_ioc_strategy = updater

    def execute(self):
        from src.spacebattle.scopes.ioc import IoC

        IoC.strategy = self._update_ioc_strategy(IoC.strategy)
