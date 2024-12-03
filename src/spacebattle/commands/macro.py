import logging
from typing import List

from src.spacebattle.commands.burn_fuel import BurnFuelCommand
from src.spacebattle.commands.change_velocity import ChangeVelocityCommand
from src.spacebattle.commands.check_fuel import CheckFuelCommand
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.move import MoveCommand
from src.spacebattle.commands.rotate import RotateCommand


class MacroCommand(Command):
    """Класс (макрокоманда) выполняющий последовательно команды из списка"""

    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        self.log = logging.getLogger(__name__)

    def execute(self):
        for command in self.commands:
            self.log.debug(f"С помощью макрокоманды выполняем команду {command}")
            command.execute()


def rotate_change_velocity_command(obj):
    """Команда для модификации вектора мгновенной скорости при повороте"""
    return MacroCommand(commands=[RotateCommand(obj), ChangeVelocityCommand(obj.velocity, obj.angular_velocity)])


def straight_line_command(obj):
    """Команда движения по прямой с расходом топлива"""
    return MacroCommand([CheckFuelCommand(obj), MoveCommand(obj), BurnFuelCommand(obj)])
