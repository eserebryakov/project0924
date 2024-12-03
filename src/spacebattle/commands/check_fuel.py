import logging

from src.spacebattle.commands.command import Command
from src.spacebattle.common import Fuel
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects import BurningObject


class CheckFuelCommand(Command):
    """Класс реализующий проверку наличия топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj
        self.log = logging.getLogger(__name__)

    def execute(self):
        gf_ = self.__obj.get_fuel()
        gfv_ = self.__obj.get_fuel_velocity()
        self.log.debug(f"Проверяем что топлива достаточно: {gf_} - {gfv_} = {gf_ - gfv_}")
        if (gf_ - gfv_) <= Fuel(0):
            raise CommandException("Недостаточно топлива")
