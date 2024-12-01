from src.spacebattle.objects import RotatingObject


class RotateCommand:
    def __init__(self, obj: RotatingObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_angle(self.__obj.get_angle() + self.__obj.get_angular_velocity())
