from abc import ABC, abstractmethod

from src.spacebattle.common.fuel import Fuel
from src.spacebattle.exceptions import CommandException

from . import Command


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


class BurnFuelCommand(Command):
    """Класс реализующий сжигание топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj

    def execute(self):
        self.__obj.set_fuel(self.__obj.get_fuel() - self.__obj.get_fuel_velocity())


class CheckFuelCommand(Command):
    """Класс реализующий проверку величины топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj

    def execute(self):
        if (self.__obj.get_fuel() - self.__obj.get_fuel_velocity()) <= Fuel(0):
            raise CommandException("Недостаточно топлива")
