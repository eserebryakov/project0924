from src.spacebattle.commands.command import Command
from src.spacebattle.common import constants
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.ioc import IoC


class RunCommand(Command):
    def __init__(self, server: ServerThread, context):
        self.__server = server
        self.__context = context

    def execute(self):
        self.__context.handle(self)

        def behaviour():
            command = self.__server.queue.get()
            try:
                command.execute()
            except Exception as e:
                IoC.resolve(constants.IOC_HANDLE_EXCEPTION, command, e).execute()
            self.__context.handle(command)

        self.__server.set_behaviour(behaviour)


"""
class RunCommand(Command):

    def __init__(self, server: ServerThread):
        self.__server = server

    def execute(self):
        def behaviour():
            command = self.__server.queue.get()
            try:
                command.execute()
            except Exception as e:
                IoC.resolve(constants.IOC_HANDLE_EXCEPTION, command, e).execute()
        self.__server.set_behaviour(behaviour)
"""
