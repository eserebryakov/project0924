from collections.abc import Callable

from src.spacebattle.commands.command import Command
from src.spacebattle.common.constants import IOC_SCOPE_CURRENT
from src.spacebattle.scopes.ioc import IoC


class RegisterDependencyCommand(Command):
    """Класс (команда) регистрирующая зависимость."""

    def __init__(self, dependency: str, strategy: Callable):
        self.dependency = dependency
        self.strategy = strategy

    def execute(self):
        current_scope = IoC.resolve(IOC_SCOPE_CURRENT)
        current_scope[self.dependency] = self.strategy
