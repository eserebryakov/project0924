import logging

from . import Command


class RetryCommand(Command):
    """Команда, которая повторяет первый раз команду"""

    def __init__(self, command: Command):
        self.command = command
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Повторяем команду {self.command}")
        self.command.execute()
