import logging

from . import Command


class WriteCommand(Command):
    """Команда, которая записывает команду в лог"""

    def __init__(self, command: Command, exception: Exception):
        self.command = command
        self.exception = exception
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Пишем исключение {self.exception} в лог")
