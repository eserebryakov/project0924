from collections import namedtuple

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.burn_fuel import BurnFuelCommand
from src.spacebattle.commands.check_fuel import CheckFuelCommand
from src.spacebattle.commands.macro import MacroCommand
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.common import Fuel, Vector
from src.spacebattle.exceptions import CommandException
from src.spacebattle.objects import BurningObject, MovingObject

DataForTest = namedtuple(
    "DataForTest", ["location_before", "velocity", "location_after", "fuel_before", "fuel_velocity", "fuel_after"]
)

_DATA_FOR_TEST = (
    DataForTest(
        location_before=Vector(1, 1),
        velocity=Vector(2, 2),
        location_after=Vector(3, 3),
        fuel_before=Fuel(2),
        fuel_velocity=Fuel(1),
        fuel_after=Fuel(1),
    ),
    DataForTest(
        location_before=Vector(1, 1),
        velocity=Vector(2, 2),
        location_after=Vector(1, 1),
        fuel_before=Fuel(2),
        fuel_velocity=Fuel(3),
        fuel_after=Fuel(2),
    ),
)


class TestStraightLineCommand:
    @pytest.fixture(params=_DATA_FOR_TEST)
    def data_for_test(self, request):
        return request.param

    @pytest.fixture
    def mock_object(self, data_for_test):
        class MockObject(MovingObject, BurningObject):
            def __init__(self):
                self.location = data_for_test.location_before
                self.velocity = data_for_test.velocity
                self.fuel = data_for_test.fuel_before
                self.fuel_velocity = data_for_test.fuel_velocity

            def get_location(self) -> Vector:
                return self.location

            def set_location(self, value: Vector) -> None:
                self.location = value

            def get_velocity(self) -> Vector:
                return self.velocity

            def get_fuel(self) -> Fuel:
                return self.fuel

            def set_fuel(self, value: Fuel) -> None:
                self.fuel = value

            def get_fuel_velocity(self) -> Fuel:
                return self.fuel_velocity

        return MockObject()

    @pytest.fixture
    def macro_command(self, mock_object):
        return MacroCommand([CheckFuelCommand(mock_object), MoveCommand(mock_object), BurnFuelCommand(mock_object)])

    def test_straight_line(self, data_for_test, macro_command, mock_object):
        try:
            macro_command.execute()
        except CommandException:
            ...
        with soft_assertions():
            assert mock_object.location == data_for_test.location_after
            assert mock_object.fuel == data_for_test.fuel_after
