import pytest

<<<<<<< HEAD
<<<<<<< HEAD
from src.spacebattle.commands.check_fuel import CheckFuelCommand
=======
from src.spacebattle.commands import CheckFuelCommand
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
=======
from src.spacebattle.commands.check_fuel import CheckFuelCommand
>>>>>>> ed1a774 (DZ4: Добавил домашнее задание по теме Команда)
from src.spacebattle.common import Fuel
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects import BurningObject


class ValidObject(BurningObject):
    """Mock класс для объекта сжигающего топлива с положительным запасом топлива"""

    def get_fuel(self) -> Fuel:
        return Fuel(5)

    def set_fuel(self, value: Fuel) -> None:
        ...

    def get_fuel_velocity(self) -> Fuel:
        return Fuel(4)


@pytest.fixture(params=[(5, 5), (5, 6)])
def invalid_object(request) -> BurningObject:
    class InvObject(BurningObject):
        """Mock класс для объекта сжигающего топлива с нехваткой топлива"""

        def get_fuel(self) -> Fuel:
            return Fuel(request.param[0])

        def set_fuel(self, value: Fuel) -> None:
            ...

        def get_fuel_velocity(self) -> Fuel:
            return Fuel(request.param[1])

    return InvObject()


class TestCheckFuel:
    def test_valid_check_fuel(self):
        """П3 Тест проверяет, что для объекта достаточно топлива"""
        obj = ValidObject()
        cfc = CheckFuelCommand(obj)
        cfc.execute()

    def test_invalid_check_fuel(self, invalid_object):
        """П3 Тест проверяет, что для объекта недостаточно топлива"""
        cfc = CheckFuelCommand(invalid_object)
        with pytest.raises(CommandException):
            cfc.execute()
