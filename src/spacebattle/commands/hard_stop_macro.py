from src.spacebattle.commands.command import Command
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.core.server import ServerThread


class HardStopMacroCommand(Command):
    def __init__(self, server: ServerThread, context):
        self.__server = server
        self.__context = context

    def execute(self):
        HardStopCommand(self.__server).execute()
