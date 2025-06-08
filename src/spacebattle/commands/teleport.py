from src.spacebattle.common.vector import Vector
from src.spacebattle.objects import TeleportableObject


class TeleportCommand:
    def __init__(self, obj: TeleportableObject, location: Vector) -> None:
        self.__obj = obj
        self.__location = location

    def execute(self):
        self.__obj.set_teleport_location(self.__location)
