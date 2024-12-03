import logging

from src.spacebattle.commands.command import Command


class Retry2Command(Command):
    """Команда, которая повторяет второй раз команду"""

    def __init__(self, command: Command):
        self.command = command
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Повторяем еще раз команду {self.command}")
        self.command.execute()
