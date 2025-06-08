import pytest

from src.spacebattle.commands.health_check import HealthCheckCommand
from src.spacebattle.common import Health
from src.spacebattle.exceptions.exeptions import CommandException
from src.spacebattle.objects.damaging import DamagingObject


class ValidObject(DamagingObject):
    def __init__(self):
        self.__health = Health(10)

    def get_health(self) -> Health:
        return self.__health

    def set_health(self, value: Health) -> None:
        self.__health = value


class TestHealthCheckCommand:
    def test_successful_health_check(self):
        obj = ValidObject()
        command = HealthCheckCommand(obj, Health(10))
        with pytest.raises(CommandException):
            command.execute()

    def test_unsuccessful_health_check(self):
        obj = ValidObject()
        command = HealthCheckCommand(obj, Health(9))
        command.execute()
