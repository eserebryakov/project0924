from queue import Queue

from src.spacebattle.commands.command import Command
from src.spacebattle.common import constants
from src.spacebattle.core.commands_mapping import COMMANDS
from src.spacebattle.core.server import ServerThread
from src.spacebattle.scopes.adapter import auto_generate_adapter
from src.spacebattle.scopes.ioc import IoC


class StartCommand(Command):
    """Класс (команда) которая создает и запускает поток."""

    def __init__(self, game_id):
        self.__game_id = game_id

    def execute(self):
        queue = Queue()
        server = ServerThread(queue)
        server.start()
        IoC.resolve(constants.IOC_REGISTER, f"{constants.IOC_THREAD}.{self.__game_id}", lambda: server).execute()
        IoC.resolve(constants.IOC_REGISTER, f"{constants.IOC_QUEUE}.{self.__game_id}", lambda: queue).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.ADAPTER, lambda class_, obj: auto_generate_adapter(class_, obj)
        ).execute()
        for command_name, command_object in COMMANDS.items():
            IoC.resolve(
                constants.IOC_REGISTER, command_name, lambda *args, cmd_obj=command_object: cmd_obj(*args)
            ).execute()
