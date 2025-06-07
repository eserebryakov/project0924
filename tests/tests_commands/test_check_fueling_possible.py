import pytest

from src.spacebattle.commands.check_fueling_possible import CheckFuelingPossibleCommand
from src.spacebattle.common import Fuel
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects.fueling import FuelingObject


class ValidObject(FuelingObject):
    """Mock класс для объекта заправляющего топливом с положительным запасом топлива"""

    def get_available_fuel(self) -> Fuel:
        return Fuel(5)

    def set_available_fuel(self, value: Fuel) -> None:
        ...


class TestCheckFuelingPossible:
    def test_valid_check_fueling_possible(self):
        """П3 Тест проверяет, что для объекта достаточно топлива"""
        obj = ValidObject()
        command = CheckFuelingPossibleCommand(obj, Fuel(5))
        command.execute()

    def test_invalid_check_fueling_possible(self):
        """П3 Тест проверяет, что для объекта недостаточно топлива"""
        command = CheckFuelingPossibleCommand(ValidObject(), Fuel(6))
        with pytest.raises(CommandException):
            command.execute()
