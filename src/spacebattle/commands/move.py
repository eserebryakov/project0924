from src.spacebattle.objects import MovingObject


class MoveCommand:
    """Класс реализующий движение"""

    def __init__(self, obj: MovingObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_location(self.__obj.get_location() + self.__obj.get_velocity())
