from abc import ABC, abstractmethod

from src.spacebattle.commands.command import Command


class Injectable(ABC):
    @abstractmethod
    def inject(self, command: Command):
        ...
