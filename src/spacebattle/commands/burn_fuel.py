import logging

from src.spacebattle.commands.command import Command
from src.spacebattle.objects import BurningObject


class BurnFuelCommand(Command):
    """Класс (команда) реализующий сжигание топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj
        self.log = logging.getLogger(__name__)

    def execute(self):
        gf_ = self.__obj.get_fuel()
        gfv_ = self.__obj.get_fuel_velocity()
        self.log.debug(f"Сжигаем топливо {gf_} на {gfv_} и получаем кол-во топлива {gf_ - gfv_}")
        self.__obj.set_fuel(gf_ - gfv_)
