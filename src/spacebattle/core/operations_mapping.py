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


def create_object(game_id, object_id, obj):
    return IoC.resolve(constants.COMMAND_CREATE_OBJECT, game_id, object_id, obj)


def moving_straight_line(game_id, object_id, args):
    object_ = IoC.resolve(constants.GAME_OBJECT, game_id, object_id)
    moving_adapter = IoC.resolve(constants.ADAPTER, MovingObject, object_)
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
    IoC.resolve(constants.COMMAND_SET_ATTRIBUTE_VALUE, object_, "velocity", args).execute()
    return IoC.resolve(constants.COMMAND_MOVING_STRAIGHT_LINE, moving_adapter)


OPERATIONS = {
    constants.OPERATION_CREATE_OBJECT: create_object,
    constants.OPERATION_MOVING_STRAIGHT_LINE: moving_straight_line,
}
