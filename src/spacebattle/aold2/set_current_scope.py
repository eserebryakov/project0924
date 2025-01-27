from src.spacebattle.aold2.scope import Scope
from src.spacebattle.commands.command import Command


class SetCurrentScopeCommand(Command):
    def __init__(self, scope: Scope, current_scope: dict):
        self.scope = scope
        self.current_scope = current_scope

    def execute(self):
        self.scope.scope = self.current_scope
