import pytest

from src.spacebattle.angle import Angle
from src.spacebattle.rotate import RotateCommand, RotatingObject


class ValidObject(RotatingObject):
    """Mock класс для поворачивающегося объекта с валидными значениями"""

    def get_angle(self) -> Angle:
        return Angle(1, 4)

    def set_angle(self, value: Angle) -> None:
        assert value == Angle(3, 4)

    def get_angular_velocity(self) -> Angle:
        return Angle(2, 4)


class InvalidAngleObject(RotatingObject):
    """
    Mock класс для поворачивающегося объекта
    у которого не возможно прочитать направление в пространстве
    """

    def get_angle(self) -> Angle:
        raise AttributeError

    def set_angle(self, value: Angle) -> None:
        ...

    def get_angular_velocity(self) -> Angle:
        ...


class InvalidAngularVelocityObject(RotatingObject):
    """
    Mock класс для поворачивающегося объекта
    у которого не возможно прочитать скорость поворота
    """

    def get_angle(self) -> Angle:
        ...

    def set_angle(self, value: Angle) -> None:
        ...

    def get_angular_velocity(self) -> Angle:
        raise AttributeError


class InvalidChangeRotationObject(RotatingObject):
    """
    Mock класс для поворачивающегося объекта
    у которого не возможно изменить направление
    """

    def get_angle(self) -> Angle:
        return Angle(1, 4)

    def set_angle(self, value: Angle) -> None:
        raise AttributeError

    def get_angular_velocity(self) -> Angle:
        return Angle(2, 4)


class TestRotate:
    def test_rotation_change(self):
        """
        П11.3 Тест проверяет, что для объекта, с направлением (1, 4) и
        поворачивающегося со скоростью (2, 4) направление в пространстве меняется на (3, 8)
        """
        obj = ValidObject()
        moc = RotateCommand(obj)
        moc.execute()

    def test_rotation_without_angle(self):
        """
        П11.3 Тест проверяет, что попытка повернуть объект,
        у которого невозможно прочитать направление в пространстве,
        приводит к ошибке
        """
        obj = InvalidAngleObject()
        moc = RotateCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_rotation_without_angular_velocity(self):
        """
        П11.3 Тест проверяет, что попытка повернуть объект,
        у которого невозможно прочитать скорость поворота,
        приводит к ошибке
        """
        obj = InvalidAngleObject()
        moc = RotateCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()

    def test_rotation_without_rotate(self):
        """
        П11.3 Тест проверяет, что попытка повернуть объект,
        у которого невозможно изменить направление, приводит к ошибке
        """
        obj = InvalidChangeRotationObject()
        moc = RotateCommand(obj)
        with pytest.raises(AttributeError):
            moc.execute()
