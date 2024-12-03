from abc import ABC, abstractmethod

from src.spacebattle.common.fuel import Fuel


class BurningObject(ABC):
    """Абстрактный класс (интерфейс) для объекта сжигающего топливо"""

    @abstractmethod
    def get_fuel(self) -> Fuel:
        ...

    @abstractmethod
    def set_fuel(self, value: Fuel) -> None:
        ...

    @abstractmethod
    def get_fuel_velocity(self) -> Fuel:
        ...
