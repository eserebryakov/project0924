from abc import ABC, abstractmethod
from typing import Optional

from src.spacebattle.commands.command import Command
from src.spacebattle.commands.hard_stop import HardStopCommand
from src.spacebattle.commands.move_to import MoveToCommand
from src.spacebattle.commands.run import RunCommand


class State(ABC):
    @abstractmethod
    def handle(self, command) -> Optional["State"]:
        ...


class NormalState(State):
    """Класс (состояние) в котором команды извлекаются и выполняются"""

    def handle(self, command) -> Optional["State"]:
        if isinstance(command, HardStopCommand):
            return None
        elif isinstance(command, MoveToCommand):
            return MoveToState()
        return self


class MoveToState(State):
    """Класс (состояние) в котором команды извлекаются из очереди и перенаправляются в другую очередь"""

    def handle(self, command) -> Optional["State"]:
        if isinstance(command, HardStopCommand):
            return None
        elif isinstance(command, RunCommand):
            return NormalState()
        return self


class Context:
    def __init__(self):
        self.__state = NormalState()

    def handle(self, command: Command):
        self.__state = self.__state.handle(command)
