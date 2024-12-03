from collections import namedtuple

import pytest
from assertpy import soft_assertions

from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
from src.spacebattle.commands.macro import MacroCommand
from src.spacebattle.commands.rotate import RotateCommand
from src.spacebattle.common import Angle, Vector
from src.spacebattle.objects import MovingObject, RotatingObject

DataForTest = namedtuple(
    "DataForTest", ["location", "velocity_after", "velocity", "angle_before", "angle_after", "angular_velocity"]
)

_DATA_FOR_TEST = (
    DataForTest(
        location=Vector(1, 1),
        velocity_after=Vector(0, 2),
        velocity=Vector(2, 0),
        angle_before=Angle(0, 4),
        angle_after=Angle(1, 4),
        angular_velocity=Angle(1, 4),
    ),
    DataForTest(
        location=Vector(1, 1),
        velocity_after=Vector(0, 0),
        velocity=Vector(0, 0),
        angle_before=Angle(0, 4),
        angle_after=Angle(1, 4),
        angular_velocity=Angle(1, 4),
    ),
)


class TestRotationChangeVelocity:
    @pytest.fixture(params=_DATA_FOR_TEST)
    def data_for_test(self, request):
        return request.param

    @pytest.fixture
    def mock_object(self, data_for_test):
        class MockObject(MovingObject, RotatingObject):
            def __init__(self):
                self.location = data_for_test.location
                self.velocity = data_for_test.velocity
                self.angle = data_for_test.angle_before
                self.angular_velocity = data_for_test.angular_velocity

            def get_location(self) -> Vector:
                return self.location

            def set_location(self, value: Vector) -> None:
                self.location = value

            def get_velocity(self) -> Vector:
                return self.velocity

            def get_angle(self) -> Angle:
                return self.angle

            def set_angle(self, value: Angle) -> None:
                self.angle = value

            def get_angular_velocity(self) -> Angle:
                return self.angular_velocity

        return MockObject()

    @pytest.fixture
    def macro_command(self, mock_object):
        return MacroCommand(
            [RotateCommand(mock_object), ChangeVelocityCommand(mock_object.velocity, mock_object.angular_velocity)]
        )

    def test_rotation_change_velocity(self, data_for_test, mock_object, macro_command):
        macro_command.execute()
        with soft_assertions():
            assert mock_object.location == data_for_test.location
            assert mock_object.velocity == data_for_test.velocity_after
            assert mock_object.angle == data_for_test.angle_after
