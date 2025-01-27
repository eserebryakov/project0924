from collections.abc import Callable

from src.spacebattle.commands.command import Command
from src.spacebattle.scopes.ioc import IoCContainer


class RegisterDependencyCommand(Command):
    def __init__(self, dependency: str, strategy: Callable):
        self.dependency = dependency
        self.strategy = strategy

    def execute(self):
        current_scope = IoCContainer.resolve("IoC.Scope.Current")
        print(current_scope)
        current_scope[self.dependency] = self.strategy
