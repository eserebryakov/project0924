from queue import Queue

from src.spacebattle.common import constants
from src.spacebattle.scopes.ioc import IoC


def spaceship_move(*args, queue: Queue):
    """Команда для постоянного движения объекта"""
    commands_list = IoC.resolve(constants.RULE_SPACESHIP_MOVE)
    commands = []
    for command in commands_list:
        commands.append(IoC.resolve(command, *args))
    macro = IoC.resolve(constants.COMMAND_MACRO, commands)
    result = IoC.resolve(constants.COMMAND_INJECTABLE)
    repeater = IoC.resolve(constants.COMMAND_PUT_COMMAND_TO_QUEUE, result, queue)
    internal_macro_command = IoC.resolve(constants.COMMAND_MACRO, [macro, repeater])
    result.inject(internal_macro_command)
    return result
