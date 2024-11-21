import logging

from . import Command


class DefaultCommand(Command):
    """Команда обработчик по умолчанию (если отсутствуют команды или исключения в обработчиках"""

    def __init__(self, command: Command, exception: Exception):
        self.log = logging.getLogger(__name__)
        self.command = command
        self.exception = exception

    def execute(self):
        self.log.debug(f"Непредвиденное исключение {self.exception} вызванное командой {self.command}")
        raise self.exception
