import logging

from src.spacebattle.commands.command import Command


class HandleExceptionCommand(Command):
    """Класс (команда) обрабатывающая исключение через Handler от другой команды"""

    def __init__(self, command: Command, exception: Exception):
        self.command = command
        self.exception = exception
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Пишем исключение {self.exception} от команды {self.command} в лог")
