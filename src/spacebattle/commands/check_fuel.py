import logging

from src.spacebattle.commands.command import Command
from src.spacebattle.common import Fuel
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects import BurningObject


class CheckFuelCommand(Command):
    """Класс (команда) реализующий проверку наличия топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj
        self.log = logging.getLogger(__name__)

    def execute(self):
        fuel_ = self.__obj.get_fuel()
        fuel_velocity = self.__obj.get_fuel_velocity()
        self.log.debug(f"Проверяем что топлива достаточно: {fuel_} - {fuel_velocity} = {fuel_ - fuel_velocity}")
        if (fuel_ - fuel_velocity) <= Fuel(0):
            raise CommandException("Недостаточно топлива")
