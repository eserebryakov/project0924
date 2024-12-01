import pytest

from src.spacebattle.commands import MoveCommand
from src.spacebattle.common.vector import Vector
from src.spacebattle.objects import MovingObject


class ValidObject(MovingObject):
    """Mock класс для движущегося объекта с валидными значениями"""

    def get_location(self) -> Vector:
        return Vector(12, 5)

    def set_location(self, value: Vector) -> None:
        assert value == Vector(5, 8)

    def get_velocity(self) -> Vector:
        return Vector(-7, 3)


class InvalidLocationObject(MovingObject):
    """Mock класс для объекта, у которого невозможно прочитать положение в пространстве"""

    def get_location(self) -> Vector:
        raise AttributeError

    def set_location(self, value: Vector) -> None:
        ...

    def get_velocity(self) -> Vector:
        ...


class InvalidVelocityObject(MovingObject):
    """Mock класс для объекта, у которого невозможно прочитать значение мгновенной скорости"""

    def get_location(self) -> Vector:
        ...

    def set_location(self, value: Vector) -> None:
        ...

    def get_velocity(self) -> Vector:
        raise AttributeError


class InvalidChangeLocationObject(MovingObject):
    """Mock класс для объекта, у которого невозможно изменить положение в пространстве"""

    def get_location(self) -> Vector:
        return Vector(1, 1)

    def set_location(self, value: Vector) -> None:
        raise AttributeError

    def get_velocity(self) -> Vector:
        return Vector(1, 1)


class TestMove:
    def test_location_change(self):
        """
        П7.3 Тест проверяет, что для объекта, находящегося в точке (12, 5) и
        движущегося со скоростью (-7, 3) движение меняет положение объекта на (5, 8)
        """
        obj = ValidObject()
        moc = MoveCommand(obj)
        moc.execute()

    def test_move_without_location(self):
        """
        П7.3 Тест проверяет, что попытка сдвинуть объект,
        у которого невозможно прочитать положение в пространстве, приводит к ошибке
        """
        obj = InvalidLocationObject()
        moc = MoveCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_move_without_velocity(self):
        """
        П7.3 Тест проверяет, что попытка сдвинуть объект, у которого невозможно
        прочитать значение мгновенной скорости, приводит к ошибке
        """
        obj = InvalidVelocityObject()
        moc = MoveCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_move_without_change_location(self):
        """
        П7.3 Тест проверяет, что попытка сдвинуть объект, у которого
        невозможно изменить положение в пространстве, приводит к ошибке
        """
        obj = InvalidChangeLocationObject()
        moc = MoveCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()
