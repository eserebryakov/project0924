from collections.abc import Callable

from src.spacebattle.commands.command import Command

# from src.spacebattle.scopes.ioc import IoCContainer


class UpdateIocResolveDependencyCommand(Command):
    def __init__(self, container, updater: Callable):
        self._container = container
        self._updater = updater

    def execute(self):
        print(self._container)
        self._container.strategy = self._updater(self._container.strategy)
        # IoCContainer.strategy = self._updater(IoCContainer.strategy)
        ...
