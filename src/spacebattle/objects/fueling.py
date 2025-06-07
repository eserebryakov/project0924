from abc import ABC, abstractmethod

from src.spacebattle.common.fuel import Fuel


class FuelingObject(ABC):
    """Абстрактный класс (интерфейс) для объекта заправляющего топливом"""

    @abstractmethod
    def get_available_fuel(self) -> Fuel:
        ...

    @abstractmethod
    def set_available_fuel(self, value: Fuel) -> None:
        ...
