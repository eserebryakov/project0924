from src.spacebattle.commands.health_reduce import HealthReduceCommand
from src.spacebattle.common import Health
from src.spacebattle.objects.damaging import DamagingObject


class ValidObject(DamagingObject):
    """Mock класс для объекта теряющего здоровье (урон)"""

    def __init__(self):
        self.__health = Health(10)

    def get_health(self) -> Health:
        return self.__health

    def set_health(self, value: Health) -> None:
        self.__health = value


class TestHealthReduceCommand:
    def test_health_reduce(self):
        """Тест проверяет что объект теряет здоровье (получает урон)"""
        obj = ValidObject()
        command = HealthReduceCommand(obj, Health(5))
        command.execute()
        assert obj.get_health() == Health(5)
