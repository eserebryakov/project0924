import logging
from typing import List

<<<<<<< HEAD
<<<<<<< HEAD
from src.spacebattle.commands.command import Command
=======
from . import Command
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
=======
from src.spacebattle.commands.command import Command
>>>>>>> ed1a774 (DZ4: Добавил домашнее задание по теме Команда)


class MacroCommand(Command):
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        self.log = logging.getLogger(__name__)

    def execute(self):
        for command in self.commands:
            self.log.debug(f"С помощью макрокоманды выполняем команду {command}")
            command.execute()
