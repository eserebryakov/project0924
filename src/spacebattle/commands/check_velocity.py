from src.spacebattle.commands.command import Command
from src.spacebattle.common.vector import Vector
from src.spacebattle.exceptions.exeptions import CommandException
from src.spacebattle.objects.moving import MovingObject


class CheckVelocityCommand(Command):
    def __init__(self, obj: MovingObject, max_velocity: Vector):
        self.__obj = obj
        self.__max_velocity = max_velocity

    def execute(self):
        if self.__max_velocity < self.__obj.get_velocity():
            raise CommandException("Превышение максимальной скорости")
