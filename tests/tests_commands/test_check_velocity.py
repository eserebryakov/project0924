import pytest

from src.spacebattle.commands.check_velocity import CheckVelocityCommand
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.common import Vector
from src.spacebattle.core.check_veolicty_decorator import with_velocity_check
from src.spacebattle.exceptions.exeptions import CommandException
from src.spacebattle.objects import MovingObject


class ExceededVelocityValidObject(MovingObject):
    """Класс (мок) объект, который НЕ превышает допустимую скорость движения"""

    def __init__(self):
        self.__location = Vector(0, 0)

    def get_location(self) -> Vector:
        return self.__location

    def set_location(self, value: Vector) -> None:
        self.__location = value

    def get_velocity(self) -> Vector:
        return Vector(100, 100)


class ExceededVelocityInvalidObject(MovingObject):
    """Класс (мок) объект, который превышает допустимую скорость движения"""

    def get_location(self) -> Vector:
        return Vector(0, 0)

    def set_location(self, value: Vector) -> None:
        assert value == Vector(101, 101)

    def get_velocity(self) -> Vector:
        return Vector(101, 101)


ExceededVelocityCommand = with_velocity_check(CheckVelocityCommand, Vector(100, 100))(MoveCommand)


class TestCheckVelocity:
    def test_successful_check_exceed_velocity(self):
        """Тест проверяет что объект движется БЕЗ превышения скорости"""
        obj_ = ExceededVelocityValidObject()
        command = ExceededVelocityCommand(obj=obj_)
        command.execute()
        assert obj_.get_velocity() == Vector(100, 100)

    def test_unsuccessful_check_exceed_velocity(self):
        """Тест проверяет что объект движется С превышением скорости"""
        obj_ = ExceededVelocityInvalidObject()
        command = ExceededVelocityCommand(obj=obj_)
        with pytest.raises(CommandException):
            command.execute()
