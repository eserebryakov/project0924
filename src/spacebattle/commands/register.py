import logging

from src.spacebattle.commands.command import Command


class RegisterCommand(Command):
    """Команда регистрирующая другую команду в хранилище команд"""

    def __init__(self, storage: dict, dependency: str, strategy) -> None:
        self.__storage = storage
        self.__dependency = dependency
        self.__strategy = strategy
        self.log = logging.getLogger(__name__)

    def execute(self) -> None:
        self.log.debug(f"Регистрируем команду '{self.__dependency}' в хранилище команд")
        self.__storage[self.__dependency] = self.__strategy
