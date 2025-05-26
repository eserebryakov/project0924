from queue import Queue

from src.spacebattle.commands.command import Command
from src.spacebattle.common.constants import IOC_REGISTER, IOC_THREAD
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.ioc import IoC


class StartCommand(Command):
    """Класс (команда) которая создает и запускает поток."""

    def execute(self):
        queue = Queue()
        server = ServerThread(queue)
        server.start()
        IoC.resolve(IOC_REGISTER, f"{IOC_THREAD}", lambda: server).execute()
