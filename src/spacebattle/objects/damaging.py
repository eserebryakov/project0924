from abc import ABC, abstractmethod

from src.spacebattle.common import Health


class DamagingObject(ABC):
    """Абстрактный класс (интерфейс) для объекта теряющего здоровье (урон)"""

    @abstractmethod
    def get_health(self) -> Health:
        ...

    @abstractmethod
    def set_health(self, value: Health) -> None:
        ...
