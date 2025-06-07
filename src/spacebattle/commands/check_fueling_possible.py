from src.spacebattle.commands.command import Command
from src.spacebattle.common import Fuel
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects import FuelingObject


class CheckFuelingPossibleCommand(Command):
    """Проверяет, что у заправщика достаточно топлива для передачи."""

    def __init__(self, fueling_obj: FuelingObject, fuel_amount: Fuel) -> None:
        self.__fueling_obj = fueling_obj
        self.__fuel_amount = fuel_amount

    def execute(self):
        current_fuel = self.__fueling_obj.get_available_fuel()
        if current_fuel < self.__fuel_amount:
            raise CommandException(
                f"Недостаточно топлива у заправщика. Нужно: {self.__fuel_amount}, есть: {current_fuel}"
            )
