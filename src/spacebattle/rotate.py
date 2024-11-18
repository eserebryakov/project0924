from abc import ABC, abstractmethod

from src.spacebattle.angle import Angle


class RotatingObject(ABC):
    """Абстрактный класс (интерфейс) для поворачивающегося объекта"""

    @abstractmethod
    def get_angle(self) -> Angle:
        ...

    @abstractmethod
    def set_angle(self, value: Angle) -> None:
        ...

    @abstractmethod
    def get_angular_velocity(self) -> Angle:
        ...


class RotateCommand:
    def __init__(self, obj: RotatingObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_angle(self.__obj.get_angle() + self.__obj.get_angular_velocity())
