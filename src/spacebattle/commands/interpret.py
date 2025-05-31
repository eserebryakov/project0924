from src.spacebattle.commands.command import Command
from src.spacebattle.common import constants
from src.spacebattle.core.operations_mapping import OPERATIONS
from src.spacebattle.scopes.ioc import IoC


class InterpretCommand(Command):
    def __init__(self, game_id, object_id, operation_id, args):
        self.__game_id = game_id
        self.__object_id = object_id
        self.__operation_id = operation_id
        self.__args = args

    def execute(self):
        command = OPERATIONS[self.__operation_id](self.__game_id, self.__object_id, self.__args)
        queue = IoC.resolve(f"{constants.IOC_QUEUE}.{self.__game_id}")
        IoC.resolve(constants.COMMAND_PUT_COMMAND_TO_QUEUE, command, queue).execute()
