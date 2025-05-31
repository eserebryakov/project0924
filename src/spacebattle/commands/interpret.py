from src.spacebattle.commands.command import Command
from src.spacebattle.commands.set_attribute_value import SetAttributeValueCommand
from src.spacebattle.common import constants
from src.spacebattle.common.vector import Vector
from src.spacebattle.objects.moving import MovingObject
from src.spacebattle.scopes.default_get_property_strategy import (
    DefaultGetPropertyStrategy,
)
from src.spacebattle.scopes.default_set_property_strategy import (
    DefaultSetPropertyStrategy,
)
from src.spacebattle.scopes.ioc import IoC


class InterpretCommand(Command):
    def __init__(self, game_id, object_id, operation_id, args):
        self.__game_id = game_id
        self.__object_id = object_id
        self.__operation_id = operation_id
        self.__args = args

    def execute(self):
        object_ = IoC.resolve(constants.GAME_OBJECT, self.__game_id, self.__object_id)
        mov_adapter = IoC.resolve(constants.ADAPTER, MovingObject, object_)
        IoC.resolve(
            constants.IOC_REGISTER,
            f"{MovingObject.__name__}.location.get",
            lambda obj: Vector(**DefaultGetPropertyStrategy(obj=obj.obj, attribute="location").resolve()),
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER,
            f"{MovingObject.__name__}.location.set",
            lambda obj, attribute, value: SetAttributeValueCommand(
                obj=obj.obj, attribute=attribute, value=value.model_dump(), strategy=DefaultSetPropertyStrategy
            ),
        ).execute()
        IoC.resolve(
            constants.IOC_REGISTER,
            f"{MovingObject.__name__}.velocity.get",
            lambda obj: Vector(**DefaultGetPropertyStrategy(obj=obj.obj, attribute="velocity").resolve()),
        ).execute()

        IoC.resolve(constants.COMMAND_SET_ATTRIBUTE_VALUE, object_, "velocity", self.__args).execute()
        command = IoC.resolve(constants.COMMAND_MOVING_STRAIGHT_LINE, mov_adapter)

        queue = IoC.resolve(f"{constants.IOC_QUEUE}.{self.__game_id}")
        IoC.resolve(constants.COMMAND_PUT_COMMAND_TO_QUEUE, command, queue).execute()
