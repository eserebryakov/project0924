from src.spacebattle.commands.command import Command
from src.spacebattle.common.health import Health
from src.spacebattle.exceptions.exeptions import CommandException
from src.spacebattle.objects import DamagingObject


class HealthCheckCommand(Command):
    """Класс (команда) проверяющая кол-во здоровья"""

    def __init__(self, obj: DamagingObject, health: Health):
        self.__obj = obj
        self.__health = health

    def execute(self):
        if self.__health >= self.__obj.get_health():
            raise CommandException("Недостаточно здоровья")
