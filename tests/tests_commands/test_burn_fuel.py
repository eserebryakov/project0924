import pytest

<<<<<<< HEAD
from src.spacebattle.commands.burn_fuel import BurnFuelCommand
=======
from src.spacebattle.commands import BurnFuelCommand
>>>>>>> d8de736 (DZ3: Добавил домашнее задание по теме Команда)
from src.spacebattle.common import Fuel
from src.spacebattle.objects import BurningObject


class ValidObject(BurningObject):
    """Mock класс для объекта сжигающего топливо с валидными значениями"""

    def get_fuel(self) -> Fuel:
        return Fuel(10)

    def set_fuel(self, value: Fuel) -> None:
        assert value == Fuel(7)

    def get_fuel_velocity(self) -> Fuel:
        return Fuel(3)


class InvalidFuelObject(BurningObject):
    """Mock класс для объекта, у которого невозможно прочитать величину топлива"""

    def get_fuel(self) -> Fuel:
        raise AttributeError

    def set_fuel(self, value: Fuel) -> None:
        ...

    def get_fuel_velocity(self) -> Fuel:
        ...


class InvalidFuelVelocityObject(BurningObject):
    """Mock класс для объекта, у которого невозможно прочитать значение мгновенной скорости расхода топлива"""

    def get_fuel(self) -> Fuel:
        ...

    def set_fuel(self, value: Fuel) -> None:
        ...

    def get_fuel_velocity(self) -> Fuel:
        raise AttributeError


class InvalidChangeFuelObject(BurningObject):
    """Mock класс для объекта, у которого невозможно изменить кол-во топлива"""

    def get_fuel(self) -> Fuel:
        return Fuel(5)

    def set_fuel(self, value: Fuel) -> None:
        raise AttributeError

    def get_fuel_velocity(self) -> Fuel:
        return Fuel(3)


class TestBurnFuel:
    def test_fuel_change(self):
        """
        П5 Тест проверяет, что для объекта, с кол-вом топлива 10 и сжигающего топливо со скоростью 3
        кол-во топлива меняется на 7
        """
        obj = ValidObject()
        moc = BurnFuelCommand(obj)
        moc.execute()

    def test_burn_without_fuel(self):
        """
        П5 Тест проверяет, что попытка сжечь топливо объекта,
        у которого невозможно прочитать текущее кол-во топлива приводит к ошибке
        """
        obj = InvalidFuelObject()
        moc = BurnFuelCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_burn_without_fuel_velocity(self):
        """
        П5 Тест проверяет, что попытка сжечь топливо объекта, у которого невозможно
        прочитать значение мгновенной скорости сжигания топлива приводит к ошибке
        """
        obj = InvalidFuelVelocityObject()
        moc = BurnFuelCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_burn_without_change_fuel(self):
        """
        П5 Тест проверяет, что попытка сжечь топливо объекта, у которого
        невозможно изменить текущее кол-во топлива, приводит к ошибке
        """
        obj = InvalidChangeFuelObject()
        moc = BurnFuelCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()
