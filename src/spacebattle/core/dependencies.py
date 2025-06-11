from queue import Queue

from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC


def spaceship_move(*args, queue: Queue):
    """Команда для постоянного движения объекта"""
    macro_move_command = IoC.resolve(
        constants.COMMAND_MACRO, [IoC.resolve(command, *args) for command in IoC.resolve(constants.RULE_SPACESHIP_MOVE)]
    )
    injectable_command = IoC.resolve(constants.COMMAND_INJECTABLE)
    put_command = IoC.resolve(constants.COMMAND_PUT_COMMAND_TO_QUEUE, injectable_command, queue)
    internal_macro_command = IoC.resolve(constants.COMMAND_MACRO, [macro_move_command, put_command])
    injectable_command.inject(internal_macro_command)
    return injectable_command
