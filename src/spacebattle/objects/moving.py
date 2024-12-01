from abc import ABC, abstractmethod

from src.spacebattle.common.vector import Vector


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
