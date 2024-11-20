import logging
from queue import Queue

from . import Command


class PutCommand(Command):
    """Команда, которая кладет команду в очередь"""

    def __init__(self, command: Command, queue: Queue):
        self.command = command
        self.queue = queue
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Положили команду {self.command} в очередь")
        self.queue.put(self.command)
