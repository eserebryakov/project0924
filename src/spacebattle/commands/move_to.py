from queue import Queue

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.run import RunCommand
from src.spacebattle.common import constants
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.ioc import IoC


class MoveToCommand(Command):
    def __init__(self, server: ServerThread, context, queue: Queue):
        self.__server = server
        self.__context = context
        self.__queue = queue

    def execute(self):
        self.__context.handle(self)

        def behaviour():
            command = self.__server.queue.get()
            if isinstance(command, (MoveToCommand, HardStopCommand, RunCommand)):
                try:
                    command.execute()
                except Exception as e:
                    IoC.resolve(constants.IOC_HANDLE_EXCEPTION, command, e).execute()
            else:
                self.__queue.put(command)
            self.__context.handle(command)

        self.__server.set_behaviour(behaviour)
