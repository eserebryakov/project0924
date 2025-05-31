from queue import Queue

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.create_object import CreateObjectCommand
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.commands.put import PutCommand
from src.spacebattle.commands.set_attribute_value import SetAttributeValueCommand
from src.spacebattle.common import constants
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
        # IoC.resolve(
        #    constants.IOC_REGISTER,
        #    f"{constants.COMMAND_CREATE_OBJECT}",
        #    lambda object_id, obj: CreateObjectCommand(object_id, obj),
        # ).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.COMMAND_SET_ATTRIBUTE_VALUE, lambda *args: SetAttributeValueCommand(*args)
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.COMMAND_MOVING_STRAIGHT_LINE, lambda *args: MoveCommand(*args)
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.COMMAND_PUT_COMMAND_TO_QUEUE, lambda *args: PutCommand(*args)
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER, constants.COMMAND_CREATE_OBJECT, lambda *args: CreateObjectCommand(*args)
        ).execute()
