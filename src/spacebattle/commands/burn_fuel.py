from abc import ABC, abstractmethod

from src.exeptions import CommandException
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
    def get_velocity(self) -> Fuel:
        ...


class BurnFuelCommand:
    """Класс реализующий сжигание топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_fuel(self.__obj.get_fuel() - self.__obj.get_velocity())


class CheckFuelCommand:
    """Класс реализующий проверку величины топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj

    def execute(self):
        if self.__obj.get_fuel() <= Fuel(0):
            raise CommandException("Недостаточно топлива")
