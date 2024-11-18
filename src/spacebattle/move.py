from abc import ABC, abstractmethod

from src.spacebattle.vector import Vector


class MovingObject(ABC):
    """Абстрактный класс (интерфейс) для движущегося объекта"""

    @abstractmethod
    def get_location(self) -> Vector:
        ...

    @abstractmethod
    def set_location(self, value: Vector) -> None:
        ...

    @abstractmethod
    def get_velocity(self) -> Vector:
        ...


class MoveCommand:
    """Класс реализующий движение"""

    def __init__(self, obj: MovingObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_location(self.__obj.get_location() + self.__obj.get_velocity())
