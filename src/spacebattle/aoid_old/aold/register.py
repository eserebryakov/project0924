import logging

from src.spacebattle.commands.command import Command


class RegisterCommand(Command):
    """Команда регистрирующая другую команду в хранилище команд"""

    def __init__(self, storage: dict, dependency: str, strategy) -> None:
        self._storage = storage
        self._dependency = dependency
        self._strategy = strategy
        self.log = logging.getLogger(__name__)

    def execute(self) -> None:
        self.log.debug(f"Регистрируем зависимость '{self._dependency}' в хранилище команд")
        self._storage[self._dependency] = self._strategy
