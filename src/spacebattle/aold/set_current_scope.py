import logging

from src.spacebattle.aold.scope import Scope
from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, scope: Scope):
        self._scope = scope
        self.log = logging.getLogger(__name__)

    def execute(self):
        self.log.debug(f"Задали текущий scope {self._scope}")
        print(f"Задали текущий scope {self._scope}")
