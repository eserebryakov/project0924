from src.spacebattle.commands.create_object import CreateObjectCommand
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.commands.put import PutCommand
from src.spacebattle.commands.set_attribute_value import SetAttributeValueCommand
from src.spacebattle.common import constants

COMMANDS = {
    constants.COMMAND_SET_ATTRIBUTE_VALUE: SetAttributeValueCommand,
    constants.COMMAND_MOVING_STRAIGHT_LINE: MoveCommand,
    constants.COMMAND_PUT_COMMAND_TO_QUEUE: PutCommand,
    constants.COMMAND_CREATE_OBJECT: CreateObjectCommand,
}
