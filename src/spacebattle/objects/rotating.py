from abc import ABC, abstractmethod

from src.spacebattle.common.angle import Angle


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
