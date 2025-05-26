from src.spacebattle.commands.command import Command
from src.spacebattle.core.server import ServerThread


class SoftStopCommand(Command):
    """Класс (команда) которая останавливает цикл выполнения команд, только после того,
    как все команды завершат свою работу"""

    def __init__(self, server: ServerThread):
        self.__server = server

    def execute(self):
        old_behaviour = self.__server.behaviour

        def new_behaviour():
            if not self.__server.queue.empty():
                old_behaviour()
            else:
                self.__server.stop()

        self.__server.set_behaviour(behaviour=new_behaviour)
