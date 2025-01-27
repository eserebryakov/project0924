from src.spacebattle.commands.command import Command


class UpdateIocResolveDependencyStrategyCommand(Command):
    def __init__(self, updater):
        self._update_ioc_strategy = updater

    def execute(self):
        from src.spacebattle.scopes.ioc import IoCContainer

        IoCContainer.strategy = self._update_ioc_strategy(IoCContainer.strategy)
