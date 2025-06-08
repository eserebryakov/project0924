from abc import ABC, abstractmethod

from src.spacebattle.common.vector import Vector


class TeleportableObject(ABC):
    """Абстрактный класс (интерфейс) для объекта мгновенной телепортации"""

    @abstractmethod
    def set_teleport_location(self, value: Vector) -> None:
        ...
