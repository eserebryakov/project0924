import logging

from src.spacebattle.commands.command import Command
from src.spacebattle.objects import BurningObject


class BurnFuelCommand(Command):
    """Класс (команда) реализующий сжигание топлива"""

    def __init__(self, obj: BurningObject) -> None:
        self.__obj = obj
        self.log = logging.getLogger(__name__)

    def execute(self):
        fuel_ = self.__obj.get_fuel()
        fuel_velocity = self.__obj.get_fuel_velocity()
        self.log.debug(f"Сжигаем топливо {fuel_} на {fuel_velocity} и получаем кол-во топлива {fuel_ - fuel_velocity}")
        self.__obj.set_fuel(fuel_ - fuel_velocity)
