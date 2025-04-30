from collections.abc import Callable

from src.spacebattle.commands.command import Command
from src.spacebattle.scopes.ioc import IoC


class RegisterDependencyCommand(Command):
    def __init__(self, dependency: str, strategy: Callable):
        self.dependency = dependency
        self.strategy = strategy

    def execute(self):
        current_scope = IoC.resolve("IoC.Scope.Current")
        current_scope[self.dependency] = self.strategy
