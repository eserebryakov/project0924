from collections.abc import Callable

from src.spacebattle.aoid3.ioc import IoCContainer

from src.spacebattle.commands.command import Command


class RegisterDependencyCommand(Command):
    def __init__(self, dependency: str, strategy: Callable):
        self.dependency = dependency
        self.strategy = strategy

    def execute(self):
        current_scope = IoCContainer.resolve("IoC.Scope.Current")
        current_scope[self.dependency] = self.strategy
