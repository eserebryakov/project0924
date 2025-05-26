from src.spacebattle.commands.command import Command
from src.spacebattle.core.server import ServerThread


class HardStopCommand(Command):
    """Класс (команда) которая останавливает цикл выполнения команд, не дожидаясь их полного завершения"""

    def __init__(self, server: ServerThread):
        self.__server = server

    def execute(self):
        self.__server.stop()
