from src.spacebattle.commands.command import Command
from src.spacebattle.common.fuel import Fuel
from src.spacebattle.objects import BurningObject, FuelingObject


class RefuelCommand(Command):
    """Класс (команда) реализующий заправку топлива"""

    def __init__(self, fueling_object: FuelingObject, burning_object: BurningObject, fuel_amount: Fuel) -> None:
        self.__fueling_object = fueling_object
        self.__burning_object = burning_object
        self.__fuel_amount = fuel_amount

    def execute(self):
        self.__fueling_object.set_available_fuel(self.__fueling_object.get_available_fuel() - self.__fuel_amount)
        self.__burning_object.set_fuel(self.__burning_object.get_fuel() + self.__fuel_amount)
