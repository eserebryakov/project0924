from src.spacebattle.commands.command import Command
from src.spacebattle.common.health import Health
from src.spacebattle.objects import DamagingObject


class HealthIncreaseCommand(Command):
    """Класс (команда) увеличивающая здоровье"""

    def __init__(self, obj: DamagingObject, health: Health):
        self.__obj = obj
        self.__health = health

    def execute(self):
        self.__obj.set_health(self.__obj.get_health() + self.__health)
